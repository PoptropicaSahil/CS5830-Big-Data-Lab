import torch
import random
from tqdm import tqdm

from utils.logging_config import var_chk_logger
from grading_tasks.task1_rotate_img import rotate


def generate_dataset(dataset, oversample_rate: float):
    images, targets = dataset.data, dataset.targets
    # var_chk_logger.debug(
    #     f"images shape = {images.shape}, targets shape = {targets.shape}"
    # )

    oversample_rate = 2 if oversample_rate < 1 else oversample_rate
    to_generate_count = images.shape[0] * (oversample_rate - 1.0)
    to_generate_count = int(to_generate_count)

    rotation_angles = [-30, -20, -10, 10, 20, 30]

    # now randomly pick a data point from the dataset
    # Randomly select data points to oversample
    # selected_indices = random.randint(
    #     0, images.shape[0], size=(to_generate_count,), dtype=torch.long
    # )

    selected_indices = random.choices(
        population=range(images.shape[0]), k=to_generate_count
    )

    # Randomly choose rotation angles
    # rotation_angles = torch.randint(-30, 31, size=(to_generate_count,), dtype=torch.int32)
    selected_angles = random.choices(population=rotation_angles, k=to_generate_count)

    # var_chk_logger.debug(
    #     f"few indices = {selected_indices[:5]}, few angles = {selected_angles[:5]}"
    # )

    # Initialize an empty list to store the updated dataset
    updated_images, updated_targets = [], []

    for idx, angle in tqdm(zip(selected_indices, selected_angles), desc="Processing images"):
        # var_chk_logger.debug(
        #     f"images[idx].shape = {images[idx].shape}, angles = {angle}"
        # )

        rotated_img = rotate(images[idx].unsqueeze(0), int(angle))
        # var_chk_logger.debug(
        #     f"rotated_img.shape = {rotated_img.shape}"
        # )
        updated_images.append(rotated_img)
        updated_targets.append(targets[idx])

    # rotate the datapoint by any one of the angles randomly
    # add the new image to the dataset
    var_chk_logger.debug(
        f"updated dataset len = {len(updated_images)}, type = {type(updated_images)}"
    )
    # var_chk_logger.debug(f"updated dataset = {updated_images}")

    updated_images = torch.cat(updated_images, dim=0)
    # var_chk_logger.debug(f"updated images shape = {updated_images.shape}")
    # var_chk_logger.debug(f"updated targets = {updated_targets[:4]}")

    updated_dataset = [(i, j) for i, j in zip(updated_images, updated_targets)]
    return updated_dataset
