import torch
import torchvision.transforms.functional as TF


def rotate(
    image: torch.Tensor,
    label,
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
    # var_chk_logger.debug(f"image and label are of types {type(image), type(label)}")
    # var_chk_logger.debug(f"image size is {image.shape}")
    # var_chk_logger.debug(f"image = {image}, label = {label}, angle = {angle}")

    # adustment for torchvision transforms, expects last dim as 1
    image = torch.unsqueeze(image, 0)
    # var_chk_logger.debug(f"new image size is {image.shape}")

    rotated_image = TF.rotate(image, angle)
    return rotated_image
