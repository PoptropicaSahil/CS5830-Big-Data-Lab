import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from grading_tasks.task2_oversample import generate_oversampled_dataset
from grading_tasks.task3_train import train_and_tune_model
from utils.data_utils import generate_data_tuple, get_datasets


@pytest.fixture
def setup_data():
    """Setup the data"""
    _, test_data = get_datasets()
    test_data = generate_data_tuple(test_data)
    data = generate_oversampled_dataset(test_data, oversample_rate=2)
    return data


def test_create_model_saving_path_directory(setup_data):
    model = train_and_tune_model(setup_data)
    # trained model dir is created
    assert os.path.exists("./trained_models/")

    # model returned is not None
    assert model is not None

    # the model with 1 conv layer and 1 linear layer exists
    assert os.path.exists("./trained_models/num_conv1_num_lin1")
