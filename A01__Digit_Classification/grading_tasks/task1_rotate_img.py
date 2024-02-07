from typing import Literal

import torch
import torchvision.transforms.functional as TF


def rotate(
    image: torch.Tensor, label, angle: Literal[-30, -20, -10, 0, 10, 20, 30]
) -> torch.Tensor:
    """
    Rotate an image by a given angle.
    0 degrees is allowed here because while constructed oversampled dataset,
    we intitilase from an empty dataset, and thus need 0-degree rotations also.

    Args:
        image (torch.Tensor): The input image tensor.
        angle (Literal[-30, -20, -10, 10, 20, 30]): The angle to rotate the image by, in degrees.

    Returns:
        torch.Tensor: The rotated image tensor.

    """
    allowed_angles = [-30, -20, -10, 0, 10, 20, 30]
    if angle not in allowed_angles:
        raise ValueError(
            "Invalid angle. Angle must be one of -30, -20, -10, 0, 10, 20, 30"
        )

    # adustment for torchvision transforms, expects last dim as 1
    image = torch.unsqueeze(image, 0)
    rotated_image = TF.rotate(image, angle)
    return rotated_image
