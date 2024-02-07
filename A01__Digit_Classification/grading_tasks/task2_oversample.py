import torch
import random
from tqdm import tqdm

from utils.logging_config import var_chk_logger
from grading_tasks.task1_rotate_img import rotate

# def generate_oversampled_dataset(dataset, oversample_rate: float):
#     images, targets, angles = dataset
#     updated_dataset = (images, targets, angles)
#     return updated_dataset

def generate_oversampled_dataset(dataset, oversample_rate: float):
    images, targets, angles = dataset
    var_chk_logger.debug(
        f"images shape = {images.shape}, targets shape = {len(targets)}, angles shape = {len(angles)}"
    )

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
        # var_chk_logger.debug(
        #     f"images[idx].shape = {images[idx].shape}, angles = {angle}"
        # )
        image = images[idx].unsqueeze(0)
        rotated_img = rotate(image, label=targets[idx], angle= int(angle))
        # var_chk_logger.debug(
        #     f"rotated_img.shape = {rotated_img.shape}"
        # )
        updated_images.append(rotated_img)
        updated_targets.append(targets[idx])
        updated_angles.append(angle)

    # rotate the datapoint by any one of the angles randomly
    # add the new image to the dataset
    var_chk_logger.debug(
        f"updated dataset len = {len(updated_images)}, type = {type(updated_images)}"
    )
    var_chk_logger.debug(
        f"updated_targets len = {len(updated_targets)}, type = {type(updated_targets)}"
    )
    var_chk_logger.debug(
        f"updated_angles len = {len(updated_angles)}, type = {type(updated_angles)}"
    )
    # var_chk_logger.debug(f"updated dataset = {updated_images}")

    updated_images = torch.cat(updated_images, dim=0)
    # var_chk_logger.debug(f"updated images shape = {updated_images.shape}")
    # var_chk_logger.debug(f"updated targets = {updated_targets[:4]}")

    updated_dataset = (updated_images, updated_targets, updated_angles)
    return updated_dataset
