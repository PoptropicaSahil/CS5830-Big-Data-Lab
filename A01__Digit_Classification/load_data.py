import os
import numpy as np
import matplotlib.pyplot as plt

import torch
from torchvision import datasets, transforms
from utils.logging_config import script_run_logger


class load_mnist_data:
    def __init__(self, save_path):
        """
        Initializes the object with a save path and sets the data_existing_flag to False.

        Parameters:
            save_path (str): The path where the data will be saved.

        Returns:
            None
        """
        self.save_path = save_path
        self.data_existing_flag = False

    def _generate_path(self):
        """
        Generate the save path for the data and log if existing data is found or created.
        """
        if not os.path.exists(self.save_path):
            script_run_logger.info(
                f"Existing data not found, creating: {self.save_path}"
            )
            os.makedirs(self.save_path)
        else:
            script_run_logger.info(f"Existing data found at {self.save_path}")
            self.data_existing_flag = True

    def get_datasets(self):
        """
        Method to get the datasets for training and testing.

        Parameters:
            self (object): The object instance
        Returns:
            tuple: A tuple containing the train dataset and test dataset
        """
        self._generate_path()

        transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        )

        # automatically checks if the data is downloaded or not
        train_dataset = datasets.MNIST(
            root=self.save_path, train=True, download=True, transform=transform
        )
        test_dataset = datasets.MNIST(
            root=self.save_path, train=False, download=True, transform=transform
        )

        return train_dataset, test_dataset

    # def plot_images_from_dataloader(self, dataset, num_images=3):
    #     data_loader = torch.utils.data.DataLoader(  # type: ignore
    #         dataset, batch_size=num_images, shuffle=True
    #     )
    #     images, labels = next(iter(data_loader))

    #     fig, axes = plt.subplots(1, num_images, figsize=(12, 3))
    #     plt.title("Few training samples")
    #     for i in range(num_images):
    #         axes[i].imshow(images[i].numpy().squeeze(), cmap="gray")
    #         axes[i].set_title(f"Label: {labels[i]}")
    #         axes[i].axis("off")

    #     plt.show()

    #     script_run_logger.info("Showing sample data points")

    #     return
