import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.model_selection import KFold, train_test_split

import shutil
import numpy as np
from utils.logging_config import var_chk_logger, script_run_logger
from torch.utils.data import Dataset


import torch.optim as optim


from torch.utils.data import DataLoader


def build_network(num_conv_layers, num_linear_layers):
    layers = []
    in_channels = 1  # assuming input is a batch of MNIST images
    for i in range(num_conv_layers):
        layers.append(nn.Conv2d(in_channels, 32, kernel_size=3, padding=1))
        layers.append(nn.ReLU())
        layers.append(nn.BatchNorm2d(32))
        in_channels = 32
    layers.append(nn.MaxPool2d(2, 2))
    layers.append(nn.Flatten())
    in_features = 32 * 28 * 28 // (2 * 2)  # since input is a 28x28 MNIST image
    for i in range(num_linear_layers):
        layers.append(nn.Linear(in_features, 128))
        layers.append(nn.ReLU())
        layers.append(nn.BatchNorm1d(128))
        layers.append(nn.Dropout(0.4))
        in_features = 128
    layers.append(nn.Linear(in_features, 10))
    layers.append(nn.LogSoftmax(dim=1))
    return nn.Sequential(*layers)


class CustomDataset(Dataset):
    def __init__(self, images, targets, angles):
        self.images = images.type(torch.float32)  # Convert to tensor
        self.targets = torch.tensor(targets, dtype=torch.float32)  # Convert to tensor
        self.angles = torch.tensor(angles, dtype=torch.float32)  # Convert to tensor

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        target = self.targets[idx]  # .item()  # Convert tensor to Python int
        angle = self.angles[idx]  # .item()  # Convert tensor to Python int

        return image, target, angle


def new_train_model(dataset):
    images, targets, angles = dataset
    var_chk_logger.debug(
        f"type(images) = {type(images)} targets = {type(targets)} angles = {type(angles)}"
    )
    var_chk_logger.debug(f"images shape = {images.shape}")

    # Step 1: Split data into training and validation sets
    (
        train_images,
        val_images,
        train_targets,
        val_targets,
        train_angles,
        val_angles,
    ) = train_test_split(images, targets, angles, test_size=0.2, random_state=42)

    train_targets = np.array(train_targets)
    train_angles = np.array(train_angles)

    var_chk_logger.debug(
        f"train_images type = {type(train_images)} shape = {train_images.shape} "
    )
    var_chk_logger.debug(
        f"train_targets type = {type(train_targets)} len = {len(train_targets)} "
    )

    k_folds = 2
    batch_size = 64
    model_saving_path = "./trained_models/"
    if not os.path.exists(model_saving_path):
        script_run_logger.info(
            f"Existing data not found, creating: {model_saving_path}"
        )
        os.makedirs(model_saving_path)
    else:
        # clear contents of the dir if it already exists
        script_run_logger.info(
            f"Existing directory found, clearing contents {model_saving_path}"
        )
        shutil.rmtree(model_saving_path)
        os.makedirs(model_saving_path)

    # model = Net()
    # model = create_cnn_model(num_num_conv_layers=2, kernel_size=2)
    # model = create_cnn(num_layers=2, kernel_size=2)

    num_conv_layers_list = [1, 2]
    num_linear_layers_list = [1, 2]

    model_perf_dict = {}

    for num_conv_layers in num_conv_layers_list:
        for num_linear_layers in num_linear_layers_list:
            model = build_network(
                num_conv_layers=num_conv_layers, num_linear_layers=num_linear_layers
            )
            # criterion = nn.CrossEntropyLoss()
            optimizer = optim.SGD(model.parameters(), lr=0.005)
            kf = KFold(n_splits=k_folds, shuffle=True)

            script_run_logger.info(
                f"\n=== Running model with {num_conv_layers} conv layers, {num_linear_layers} linear layers ==="
            )

            for fold, (train_index, val_index) in enumerate(kf.split(train_images)):
                script_run_logger.info(f"Fold {fold+1}:")

                train_images_fold = train_images[train_index]
                # var_chk_logger.debug(
                #     f"train_images_fold type = {type(train_images_fold)} shape = {train_images_fold.shape} "
                # )
                train_targets_fold = train_targets[train_index]
                train_angles_fold = train_angles[train_index]

                val_images_fold = train_images[val_index]
                val_targets_fold = train_targets[val_index]
                val_angles_fold = train_angles[val_index]

                # Create training DataLoader
                train_dataset = CustomDataset(
                    train_images_fold, train_targets_fold, train_angles_fold
                )
                train_loader = DataLoader(
                    train_dataset, batch_size=batch_size, shuffle=True
                )

                # Create validation DataLoader
                val_dataset = CustomDataset(
                    val_images_fold, val_targets_fold, val_angles_fold
                )
                val_loader = DataLoader(
                    val_dataset, batch_size=batch_size, shuffle=False
                )

                # var_chk_logger.debug("created dataloaders")

                # training
                model.train()
                for batch_idx, (data, target, angle) in enumerate(train_loader):
                    data, target, _ = data, target, angle
                    # var_chk_logger.debug(f"data shape = {data.shape}, target shape = {target.shape}")
                    optimizer.zero_grad()
                    output = model(data)
                    # pred = output.argmax(dim=1, keepdim=True)
                    loss = F.nll_loss(output, target.type(torch.LongTensor))
                    loss.backward()
                    optimizer.step()

                    if batch_idx % 100 == 0:
                        # script_run_logger.info(f"batch_idx = {batch_idx}, loss = {loss.item()}")
                        script_run_logger.info(
                            f"Train Epoch: [{batch_idx}/{ len(train_loader)} ({100. * batch_idx / len(train_loader):.2f}%)]\tLoss: {loss:.4f}"
                        )

                # validation
                test_loss = 0
                correct = 0
                total = 0
                model.eval()
                for batch_idx, (data, target, angle) in enumerate(val_loader):
                    data, target, _ = data, target, angle
                    output = model(data)
                    test_loss += F.nll_loss(
                        output, target.type(torch.LongTensor)
                    ).item()  # sum up batch loss
                    pred = output.argmax(
                        dim=1, keepdim=True
                    )  # get the index of the max log-probability
                    correct += pred.eq(target.view_as(pred)).sum().item()
                    total += target.size(0)

                    if batch_idx % 100 == 0:
                        # script_run_logger.info(f"batch_idx = {batch_idx}, loss = {loss.item()}")
                        script_run_logger.info(
                            f"Test Epoch: [{batch_idx}/{ len(val_loader)} ({100. * batch_idx / len(val_loader):.2f}%)]"
                        )

                test_loss /= len(val_loader)
                script_run_logger.info(
                    f"Test set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{total} ({100*correct/total:.0f}%)"
                )

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

    script_run_logger.info("Fetched best model from saved models")
    return model
