import torch
import torchvision.transforms.functional as TF


def rotate(
    image: torch.Tensor,
    angle,
    # : Literal[-30, -20, -10, 10, 20, 30]
) -> torch.Tensor:
    """
    Rotate an image by a given angle.

    Args:
        image (torch.Tensor): The input image tensor.
        angle (Literal[-30, -20, -10, 10, 20, 30]): The angle to rotate the image by, in degrees.

    Returns:
        torch.Tensor: The rotated image tensor.

    """
    rotated_image = TF.rotate(image, angle)
    return rotated_image
