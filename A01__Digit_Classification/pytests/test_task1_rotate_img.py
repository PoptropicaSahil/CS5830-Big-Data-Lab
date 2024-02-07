import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import torch
from grading_tasks.task1_rotate_img import rotate


def test_rotate_():
    # Test rotating the image by -30 degrees
    image = torch.rand(1, 256, 256)  # Example image tensor
    rotated_image = rotate(image, None, -30)
    assert rotated_image.shape == (1, 1, 256, 256)  # Check if the shape is correct

def test_rotate_three_channel():
    # Test rotating the image by 20 degrees and 3 channel image
    image = torch.rand(3, 256, 256)  # Example image tensor
    rotated_image = rotate(image, None, 20)
    assert rotated_image.shape == (1, 3, 256, 256)  # Check if the shape is correct

def test_rotate_invalid_angle():
    # Test passing invalid angle
    image = torch.rand(3, 256, 256)  # Example image tensor
    with pytest.raises(ValueError):
        # Passing an angle not in the specified range
        rotate(image, None, 45)  # type: ignore
