import os

import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from torchvision import datasets, transforms
from utils.logging_config import script_run_logger, var_chk_logger


def plot_random_samples_from_data(dataset):
    images, targets, angles = dataset
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    plt.title("Few training samples")
    for i in range(3):
        axes[i].imshow(images[i].numpy().squeeze(), cmap="gray")
        axes[i].set_title(f"Label: {targets[i]}, Angle: {angles[i]}")
        axes[i].axis("off")
    plt.show()
    script_run_logger.info("Showing sample data points")
    return


def plot_image(image, label=None, angle=None):
    var_chk_logger.debug(f"image type = {type(image)}, label = {label}")
    # fig, axes = plt.plot(figsize=(12, 3))
    title = f"Plot given figure \n Label: {label}, angle = {angle}"
    plt.title(title)
    plt.imshow(image.numpy().squeeze(), cmap="gray")
    plt.axis("off")
    plt.show()


def get_datasets(save_path):
    if not os.path.exists(save_path):
        script_run_logger.info(f"Existing data not found, creating: {save_path}")
        os.makedirs(save_path)
    else:
        script_run_logger.info(f"Existing data found at {save_path}")

    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )

    # automatically checks if the data is downloaded or not
    train_dataset = datasets.MNIST(
        root=save_path, train=True, download=True, transform=transform
    )
    test_dataset = datasets.MNIST(
        root=save_path, train=False, download=True, transform=transform
    )

    return train_dataset, test_dataset


def generate_data_tuple(dataset):
    images, targets = dataset.data, dataset.targets
    angles = [int(0)] * len(targets)
    dataset = images, targets, angles
    return dataset


def generate_dataset_sample(dataset, n_samples=1000):
    random_state = 42
    images, targets, angles = dataset
    (
        _,
        images_sample,
        _,
        targets_sample,
        _,
        angles_sample,
    ) = train_test_split(
        images, targets, angles, test_size=n_samples, random_state=random_state
    )

    sample_set = (images_sample, targets_sample, angles_sample)
    return sample_set


def generate_dataset_by_angle(dataset, angle_value):
    images, targets, angles = dataset
    filter_idx = np.where(np.array(angles) == angle_value)[0]

    filtered_images = images[filter_idx]
    filtered_targets = [targets[i] for i in filter_idx]
    filtered_angles = [angles[i] for i in filter_idx]

    return (filtered_images, filtered_targets, filtered_angles)


def generate_holdout_set(dataset, holdout_size=1000):
    images, targets, angles = dataset
    var_chk_logger.debug(
        f"type(images) = {type(images)} targets = {type(targets)} angles = {type(angles)}"
    )

    var_chk_logger.debug(f"images shape = {images.shape}")

    random_state = 42

    # Split the dataset into training/validation and testing sets
    (
        images,
        images_sample,
        targets,
        targets_sample,
        angles,
        angles_sample,
    ) = train_test_split(
        images, targets, angles, test_size=holdout_size, random_state=random_state
    )

    sample_set = (images_sample, targets_sample, angles_sample)
    remaining_set = (images, targets, angles)

    var_chk_logger.debug(
        f"shape images_sample= {images_sample.shape}, len targets_sample = {len(targets_sample)}"
    )

    return sample_set, remaining_set
