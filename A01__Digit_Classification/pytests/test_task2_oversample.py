import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from grading_tasks.task2_oversample import generate_oversampled_dataset
from utils.data_utils import generate_data_tuple, get_datasets


@pytest.fixture
def setup_data():
    _, test_data = get_datasets()
    test_data = generate_data_tuple(test_data)
    return test_data


def test_oversample_data_ratetype(setup_data):
    """Check if type matches"""
    with pytest.raises(TypeError):
        # Passing an angle not in the specified range
        oversampled_data = generate_oversampled_dataset(setup_data, oversample_rate="2") # type: ignore


def test_oversample_data_shape(setup_data):
    """Check if type matches"""
    oversampled_data = generate_oversampled_dataset(setup_data, oversample_rate=2)
    assert isinstance(oversampled_data, tuple)
    assert isinstance(oversampled_data[1], list)


def test_oversample_2(setup_data):
    """Check if the images remain the same with oversample rate of 2"""
    oversampled_data = generate_oversampled_dataset(setup_data, oversample_rate=2)
    assert len(oversampled_data[1]) == len(setup_data[1])


def test_oversample_4(setup_data):
    """Check if the images increase with oversample rate of 4"""
    oversampled_data = generate_oversampled_dataset(setup_data, oversample_rate=4)
    assert len(oversampled_data[1]) == 3 * len(setup_data[1])


def test_oversample_half(setup_data):
    """Check if the images remain the same with oversample rate of 0.5"""
    oversampled_data = generate_oversampled_dataset(setup_data, oversample_rate=0.5)
    assert len(oversampled_data[1]) == len(setup_data[1])
