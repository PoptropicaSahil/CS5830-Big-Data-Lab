# main_script.py
import argparse

from grading_tasks.task1_rotate_img import rotate
from grading_tasks.task2_oversample import generate_oversampled_dataset
from grading_tasks.task3_train import train_and_tune_model
from grading_tasks.task4_monitoring import monitor_perf
from utils.data_utils import (  # generate_dataset_sample,
    clear_plots_dir,
    generate_data_tuple,
    generate_dataset_by_angle,
    generate_holdout_set,
    get_datasets,
    plot_image,
    plot_random_samples_from_data,
)

# from train_classifier import train_classifier
from utils.logging_config import script_run_logger
from utils.performance_metrics import generate_performance_metrics


def main():
    parser = argparse.ArgumentParser(
        description="Load MNIST dataset and train a classifier"
    )

    parser.add_argument(
        "--oversample_rate",
        type=float,
        default=8,
        help="Oversampling rate. Use 8 for 490k images",
    )

    args = parser.parse_args()

    # Input checks for argument
    if not 0 < args.oversample_rate < 100:
        raise argparse.ArgumentTypeError("oversample_rate is out of bounds")

    # Load datasets
    data_dir = "./data"
    train_data, test_data = get_datasets(save_path=data_dir)
    script_run_logger.info("MNIST dataset loaded successfully")

    # Convert dataset to the format used in the experiments below
    # (images, targets, angles)
    train_data = generate_data_tuple(train_data)
    test_data = generate_data_tuple(test_data)
    script_run_logger.info("Converted data to tuple form")

    # Clear directory for plots
    clear_plots_dir()

    # Show few images from training data
    plot_random_samples_from_data(train_data)

    script_run_logger.info(
        f"Size of train data: {len(train_data[0])}, test data: {len(test_data[0])}"
    )

    ### TASK 1 ###
    # simple example to show rotation of data of a random sample
    rotation_angle = 30
    images, labels, angles = train_data
    random_idx = 1000
    image, label, angle = images[random_idx], labels[random_idx], angles[random_idx]

    plot_image(image, label, angle)
    new_img = rotate(image, label, angle=rotation_angle)
    plot_image(new_img, label, angle=rotation_angle)

    # use smaller data for faster experiments
    # n_samples = 10000
    # train_data = generate_dataset_sample(train_data, n_samples=n_samples)
    # test_data = generate_dataset_sample(test_data, n_samples=n_samples // 4)
    # script_run_logger.debug(f"using sample of {n_samples} datapoints ")

    ### TASK 2 ###
    # Generate oversampled data
    # Use 8 for 490k images
    oversample_rate = args.oversample_rate
    train_data = generate_oversampled_dataset(
        train_data, oversample_rate=oversample_rate
    )
    test_data = generate_oversampled_dataset(test_data, oversample_rate=oversample_rate)
    script_run_logger.info(f"Oversampled train data, size = {len(train_data[0])}")
    script_run_logger.info(f"Oversampled test data, size = {len(test_data[0])}")

    # Generate holdout sets
    holdout_size = 5000
    holdout_set, train_data = generate_holdout_set(
        train_data, holdout_size=holdout_size
    )
    script_run_logger.info(f"Updated holdout data size = {len(holdout_set[0])}")
    script_run_logger.info(f"Updated train data size = {len(train_data[0])}")

    # Generate dataset by specific angles
    train_data_0 = generate_dataset_by_angle(train_data, angle_value=0)
    test_data_0 = generate_dataset_by_angle(test_data, angle_value=0)
    holdout_set_0 = generate_dataset_by_angle(holdout_set, angle_value=0)

    ### TASK 3 and 4 ###
    script_run_logger.info("Check training log file for training logs")

    threshold = 0.15
    # Start with 0 degrees and ground truth of 10 degrees
    script_run_logger.warning("Training on set of 0 degrees rotation")
    model = train_and_tune_model(dataset=train_data_0)
    script_run_logger.warning("Checking performance on holdout set of 0 degrees")
    flag = monitor_perf(model, holdout_set_0, threshold=threshold)
    train_data_0_10 = generate_dataset_by_angle(train_data, angle_value=[0, 10])
    test_data_0_10 = generate_dataset_by_angle(test_data, angle_value=[0, 10])
    holdout_set_10 = generate_dataset_by_angle(holdout_set, angle_value=[10])
    script_run_logger.warning("Checking performance on holdout set of 10 degrees")
    flag = monitor_perf(model, holdout_set_10, threshold=threshold)

    script_run_logger.warning("Training on set of 0 and 10 degrees")
    model = train_and_tune_model(dataset=train_data_0_10)
    script_run_logger.warning("Checking performance on holdout set of 10 degrees")
    flag = monitor_perf(model, holdout_set_10, threshold=threshold)

    # Ground truth of -30 degrees
    train_data_0_10_n30 = generate_dataset_by_angle(
        train_data, angle_value=[0, 10, -30]
    )
    test_data_0_10_n30 = generate_dataset_by_angle(test_data, angle_value=[0, 10, -30])
    holdout_set_n30 = generate_dataset_by_angle(holdout_set, angle_value=[-30])
    script_run_logger.warning("Checking performance on holdout set of -30 degrees")
    flag = monitor_perf(model, holdout_set_n30, threshold=threshold)

    script_run_logger.warning("Training on set of 0 and 10 and -30 degrees")
    model = train_and_tune_model(dataset=train_data_0_10_n30)

    script_run_logger.warning(
        "Checking performance on holdout set of 0 and 10 and -30 degrees"
    )
    flag = monitor_perf(model, holdout_set_n30, threshold=threshold)

    # Ground truth of 20 degrees
    holdout_set_20 = generate_dataset_by_angle(holdout_set, angle_value=[20])
    script_run_logger.warning("Checking performance on holdout set of 20 degrees")
    flag = monitor_perf(model, holdout_set_20, threshold=threshold)

    # Train on full dataset
    script_run_logger.warning("Training on full train set")
    model = train_and_tune_model(dataset=train_data)
    script_run_logger.warning("Checking performance on full holdout set")
    flag = monitor_perf(model, holdout_set, threshold=threshold)

    script_run_logger.info("Generating performance metrics")
    generate_performance_metrics(model, holdout_set)


if __name__ == "__main__":
    main()
