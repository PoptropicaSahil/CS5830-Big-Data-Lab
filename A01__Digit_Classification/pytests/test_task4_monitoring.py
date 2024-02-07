import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import torch
from grading_tasks.task2_oversample import generate_oversampled_dataset
from grading_tasks.task3_train import train_and_tune_model
from grading_tasks.task4_monitoring import monitor_perf
from utils.data_utils import generate_data_tuple, get_datasets


@pytest.fixture
def setup_data():
    """Setup the data"""
    train_data, test_data = get_datasets()
    train_data = generate_data_tuple(train_data)
    test_data = generate_data_tuple(test_data)

    train_data = generate_oversampled_dataset(train_data, oversample_rate=2)
    test_data = generate_oversampled_dataset(test_data, oversample_rate=2)
    model = train_and_tune_model(train_data)

    return model, test_data


def test_loss_more_than_threshold(setup_data):
    """
    Check loss is more than threshold (i.e. flag raised)
    when ground truth is bad
    """
    model, test_data = setup_data
    bad_dataset = (
        torch.randn(10, 1, 28, 28),
        list(range(10)),
        [0] * 10,
    )
    threshold = 0.30
    flag = monitor_perf(model, ground_truth_dataset=bad_dataset, threshold=threshold)
    assert flag == 1


def test_loss_less_than_threshold(setup_data):
    """
    Check loss is less than threshold (i.e. flag not raised)
    when ground truth is good
    """
    model, test_data = setup_data
    threshold = 0.30
    flag = monitor_perf(model, ground_truth_dataset=test_data, threshold=threshold)
    assert flag == 0