# main_script.py
import argparse


# from train_classifier import train_classifier
from utils.logging_config import script_run_logger, var_chk_logger

from utils.data_utils import plot_image
from utils.data_utils import (
    get_datasets,
    generate_holdout_set,
    generate_data_tuple,
    generate_dataset_sample,
)

from grading_tasks.task1_rotate_img import rotate
from grading_tasks.task2_oversample import generate_oversampled_dataset
from grading_tasks.task3_train import new_train_model
from grading_tasks.task4_monitoring import monitor_perf


def main():
    parser = argparse.ArgumentParser(
        description="Load MNIST dataset and train a classifier"
    )
    parser.add_argument(
        "--data_dir", type=str, default="./data", help="Path to load MNIST dataset"
    )
    parser.add_argument(
        "--epochs", type=int, default=5, help="Number of training epochs"
    )
    parser.add_argument(
        "--batch_size", type=int, default=128, help="Batch size for training"
    )
    parser.add_argument(
        "--learning_rate", type=float, default=0.01, help="Learning rate for optimizer"
    )
    args = parser.parse_args()

    # Load MNIST dataset
    script_run_logger.info(f"args.data_dir is {args.data_dir}")
    script_run_logger.info(f"args.learning_rate is {args.learning_rate}")
    script_run_logger.info(f"args.epochs is {args.epochs}")

    # data_loader = load_mnist_data(save_path=args.data_dir)
    train_data, test_data = get_datasets(save_path=args.data_dir)
    script_run_logger.info("MNIST dataset loaded successfully.")

    train_data = generate_data_tuple(train_data)
    test_data = generate_data_tuple(test_data)
    script_run_logger.debug("converted data to tuple form")

    # Show few images from training data
    # data_loader.plot_images_from_dataloader(train_data)

    script_run_logger.info(
        f"Size of train data: {len(train_data)}, test data: {len(test_data)}"
    )

    # var_chk_logger.debug(
    #     f"image and labels are {[(type(image), type(label)) for image, label in train_data][:3]}"
    # )

    rotation_angle = 30
    images, labels, angles = train_data
    image = images[0]
    label = labels[0]
    angle = angles[0]

    var_chk_logger.debug(f"image and label are of types {type(image), type(label)}")
    var_chk_logger.debug(f"image size is {image.shape}")

    plot_image(image, label, angle)

    new_img = rotate(image, label, angle=rotation_angle)
    plot_image(new_img, label, angle=rotation_angle)

    n_samples = 10000
    train_data = generate_dataset_sample(train_data, n_samples=n_samples)
    test_data = generate_dataset_sample(test_data, n_samples=n_samples // 4)

    script_run_logger.debug(f"using sample of {n_samples} datapoints ")

    oversample_rate = 8
    # change to 8 for 490k images

    updated_train_data = generate_oversampled_dataset(
        train_data, oversample_rate=oversample_rate
    )  # [(updated_images, updated_targets, updated_angles)]
    script_run_logger.info(
        f"Oversampled train data, size = {len(updated_train_data[0])}"
    )

    updated_test_data = generate_oversampled_dataset(
        test_data, oversample_rate=oversample_rate
    )
    script_run_logger.info(f"Oversampled test data, size = {len(updated_test_data[0])}")

    holdout_size = 5000
    holdout_set, updated_train_data = generate_holdout_set(
        updated_train_data, holdout_size=holdout_size
    )
    script_run_logger.info(f"Updated holdout data size = {len(holdout_set[0])}")
    script_run_logger.info(f"Updated train data size = {len(updated_train_data[0])}")

    # learn_model(dataset=updated_train_data)
    model = new_train_model(dataset=updated_train_data)
    script_run_logger.info("Fetched best model in main script")

    flag = monitor_perf(model, holdout_set, threshold=0.13)
    script_run_logger.info(f"Got flag value {flag}")


if __name__ == "__main__":
    main()
