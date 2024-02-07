import os
import shutil

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from sklearn.model_selection import KFold
from torch.utils.data import DataLoader, Dataset
from utils.logging_config import script_run_logger, train_run_logger


class CustomDataset(Dataset):
    """Usual pytorch dataset class for using custom datasets"""

    def __init__(self, images, targets, angles):
        # Convert to tensor.float32 only for training
        self.images = images.type(torch.float32)
        self.targets = torch.tensor(targets, dtype=torch.float32)
        self.angles = torch.tensor(angles, dtype=torch.float32)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        target = self.targets[idx]
        angle = self.angles[idx]

        return image, target, angle


def build_network(num_conv_layers: int, num_linear_layers: int):
    """
    Builds a neural network with the specified number of convolutional and linear layers.

    Args:
        num_conv_layers (int): The number of convolutional layers.
        num_linear_layers (int): The number of linear layers.

    Returns:
        nn.Sequential: A sequential container with the layers of the neural network.
    """
    layers = []
    in_channels = 1  #  input is a batch of MNIST images (1 channel only)
    for i in range(num_conv_layers):
        layers.append(nn.Conv2d(in_channels, 32, kernel_size=3, padding=1))
        layers.append(nn.ReLU())
        layers.append(nn.BatchNorm2d(32))
        in_channels = 32
    layers.append(nn.MaxPool2d(2, 2))
    layers.append(nn.Flatten())
    in_features = 32 * 28 * 28 // (2 * 2)  # since input is a 28 x 28 MNIST image
    for i in range(num_linear_layers):
        layers.append(nn.Linear(in_features, 128))
        layers.append(nn.ReLU())
        layers.append(nn.BatchNorm1d(128))
        layers.append(nn.Dropout(0.4))
        in_features = 128
    layers.append(nn.Linear(in_features, 10))
    layers.append(nn.LogSoftmax(dim=1))
    return nn.Sequential(*layers)


def train_loop(train_loader, optimizer, model):
    """Train the model for one epoch"""
    model.train()
    for batch_idx, (data, target, angle) in enumerate(train_loader):
        data, target, _ = data, target, angle
        optimizer.zero_grad()
        output = model(data)
        # pred = output.argmax(dim=1, keepdim=True)
        loss = F.nll_loss(output, target.type(torch.LongTensor))
        loss.backward()
        optimizer.step()

        if batch_idx % 200 == 0:
            train_run_logger.info(
                f"Train Epoch: [{batch_idx}/{ len(train_loader)} ({100. * batch_idx / len(train_loader):.2f}%)]\tLoss: {loss:.4f}"
            )


def eval_loop(val_loader, model):
    """Evaluate the model for on valiadtion dataloader"""

    model.eval()
    test_loss = 0
    correct = 0
    total = 0

    for batch_idx, (data, target, angle) in enumerate(val_loader):
        data, target, _ = data, target, angle
        output = model(data)
        # sum up batch loss
        test_loss += F.nll_loss(output, target.type(torch.LongTensor)).item()
        # get the index of the max log-probability
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
        total += target.size(0)

        if batch_idx % 200 == 0:
            train_run_logger.info(
                f"Test Epoch: [{batch_idx}/{ len(val_loader)} ({100. * batch_idx / len(val_loader):.2f}%)]"
            )

    test_loss /= len(val_loader)
    script_run_logger.info(
        f"Test set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{total} ({100*correct/total:.2f}%)"
    )
    return test_loss


def train_and_tune_model(dataset: tuple):
    """Train and tune a model using the given dataset."""

    images, targets, angles = dataset
    train_targets = np.array(targets)
    train_angles = np.array(angles)

    k_folds = 2
    batch_size = 64
    model_saving_path = "./trained_models/"

    # Make dir if does not exist, else clear
    if not os.path.exists(model_saving_path):
        script_run_logger.info(
            f"Existing data not found, creating: {model_saving_path}"
        )
        os.makedirs(model_saving_path)
    else:
        script_run_logger.info(
            f"Existing directory found, clearing contents {model_saving_path}"
        )
        shutil.rmtree(model_saving_path)
        os.makedirs(model_saving_path)

    # hyperparameters to be tested
    num_conv_layers_list = [1, 2]
    num_linear_layers_list = [1, 2]

    # dict for storing model performances
    model_perf_dict = {}

    # loop over hyperparameters
    for num_conv_layers in num_conv_layers_list:
        for num_linear_layers in num_linear_layers_list:
            # Setup model and optimizer
            model = build_network(
                num_conv_layers=num_conv_layers, num_linear_layers=num_linear_layers
            )
            optimizer = optim.SGD(model.parameters(), lr=0.005)
            kf = KFold(n_splits=k_folds, shuffle=True)

            script_run_logger.info(
                f"=== Running model with {num_conv_layers} conv layers, {num_linear_layers} linear layers ==="
            )
            train_run_logger.info(
                f"\n=== Running model with {num_conv_layers} conv layers, {num_linear_layers} linear layers ==="
            )

            for fold, (train_index, val_index) in enumerate(kf.split(images)):
                script_run_logger.info(f"Training fold {fold+1}:")

                images_fold = images[train_index]
                train_targets_fold = train_targets[train_index]
                train_angles_fold = train_angles[train_index]

                val_images_fold = images[val_index]
                val_targets_fold = train_targets[val_index]
                val_angles_fold = train_angles[val_index]

                # Create training DataLoader
                train_dataset = CustomDataset(
                    images_fold, train_targets_fold, train_angles_fold
                )
                train_loader = DataLoader(
                    train_dataset, batch_size=batch_size, shuffle=True
                )

                # Create validation DataLoader
                val_dataset = CustomDataset(
                    val_images_fold, val_targets_fold, val_angles_fold
                )
                val_loader = DataLoader(
                    val_dataset, batch_size=batch_size * 2, shuffle=False
                )

                # training
                train_loop(train_loader, optimizer, model)
                # validation
                test_loss = eval_loop(val_loader, model)

            torch.save(
                model.state_dict(),
                model_saving_path
                + f"num_conv{num_conv_layers}_num_lin{num_linear_layers}",
            )

            #  add test loss and accuracy to dict
            model_perf_dict[f"{num_conv_layers}_{num_linear_layers}"] = test_loss  # type: ignore

            script_run_logger.info(
                "Saved model state and updated with model performance logs\n"
            )

    # get model with least test loss
    best_model_name = min(model_perf_dict, key=model_perf_dict.get)  # type: ignore
    num_conv_layers, num_linear_layers = best_model_name.split("_")

    script_run_logger.info(
        f"Fetched best model config: num_conv_layers = {num_conv_layers}, num_linear_layers = {num_linear_layers}"
    )

    # fetch best model
    model = build_network(
        num_conv_layers=int(num_conv_layers), num_linear_layers=int(num_linear_layers)
    )
    model.load_state_dict(
        torch.load(
            model_saving_path + f"num_conv{num_conv_layers}_num_lin{num_linear_layers}"
        )
    )

    return model
