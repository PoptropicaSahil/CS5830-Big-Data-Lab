import random

import torch
from grading_tasks.task1_rotate_img import rotate
from tqdm import tqdm
from utils.logging_config import var_chk_logger


def generate_oversampled_dataset(dataset: tuple, oversample_rate: float) -> tuple:
    """Generate an oversampled dataset based on the input dataset and oversample rate"""
    images, targets, angles = dataset
    oversample_rate = 2 if oversample_rate < 1 else oversample_rate
    to_generate_count = images.shape[0] * (oversample_rate - 1.0)
    to_generate_count = int(to_generate_count)

    rotation_angles = [-30, -20, -10, 0, 10, 20, 30]
    selected_indices = random.choices(
        population=range(images.shape[0]), k=to_generate_count
    )
    selected_angles = random.choices(population=rotation_angles, k=to_generate_count)

    # Initialize an empty list to store the updated dataset
    updated_images, updated_targets, updated_angles = [], [], []

    for idx, angle in tqdm(
        zip(selected_indices, selected_angles),
        desc=f"Processing images at oversample rate {oversample_rate}",
        total=to_generate_count,
    ):
        image = images[idx].unsqueeze(0)
        rotated_img = rotate(image, label=targets[idx], angle=angle)
        updated_images.append(rotated_img)
        updated_targets.append(targets[idx])
        updated_angles.append(angle)

    # rotate the datapoint by any one of the angles randomly
    # add the new image to the dataset
    var_chk_logger.debug(f"Updated oversampled dataset size = {len(updated_images)})")
    updated_images = torch.cat(updated_images, dim=0)
    updated_dataset = (updated_images, updated_targets, updated_angles)
    return updated_dataset
