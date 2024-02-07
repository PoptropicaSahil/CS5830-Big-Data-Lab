# main_script.py
import argparse

from grading_tasks.task1_rotate_img import rotate
from grading_tasks.task2_oversample import generate_oversampled_dataset
from grading_tasks.task3_train import train_and_tune_model
from grading_tasks.task4_monitoring import monitor_perf
from utils.data_utils import (
    generate_data_tuple,
    generate_dataset_by_angle,
    generate_dataset_sample,
    generate_holdout_set,
    get_datasets,
    plot_image,
)

# from train_classifier import train_classifier
from utils.logging_config import script_run_logger, var_chk_logger


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

    oversample_rate = 5
    # change to 8 for 490k images

    train_data = generate_oversampled_dataset(
        train_data, oversample_rate=oversample_rate
    )  # [(images, targets, angles)]
    script_run_logger.info(f"Oversampled train data, size = {len(train_data[0])}")

    test_data = generate_oversampled_dataset(test_data, oversample_rate=oversample_rate)
    script_run_logger.info(f"Oversampled test data, size = {len(test_data[0])}")

    holdout_size = 5000
    holdout_set, train_data = generate_holdout_set(
        train_data, holdout_size=holdout_size
    )
    script_run_logger.info(f"Updated holdout data size = {len(holdout_set[0])}")
    script_run_logger.info(f"Updated train data size = {len(train_data[0])}")

    train_data_0 = generate_dataset_by_angle(train_data, angle_value=0)
    test_data_0 = generate_dataset_by_angle(test_data, angle_value=0)
    holdout_set_0 = generate_dataset_by_angle(holdout_set, angle_value=0)

    script_run_logger.info(f"Updated angle 0 data size = {train_data_0[0].shape}")
    script_run_logger.info(
        f"Updated holdout_set_0 data size = {holdout_set_0[0].shape}"
    )

    train_data_10 = generate_dataset_by_angle(train_data, angle_value=10)
    test_data_10 = generate_dataset_by_angle(test_data, angle_value=10)
    holdout_set_10 = generate_dataset_by_angle(holdout_set, angle_value=10)

    script_run_logger.info(f"Updated angle 10 data size = {train_data_10[0].shape}")
    script_run_logger.info(
        f"Updated holdout_set_10 data size = {holdout_set_10[0].shape}"
    )

    model = train_and_tune_model(dataset=train_data_0)

    # so that not commented out
    # random_flag = 1
    # if not random_flag:
    #     model = train_and_tune_model(dataset=train_data_0)

    ###### shortcut for now ######
    # import torch
    # from grading_tasks.task3_train import build_network

    # model = build_network(num_conv_layers=2, num_linear_layers=2)
    # model_saving_path = "./trained_models/"
    # model.load_state_dict(torch.load(model_saving_path + "num_conv2_num_lin2"))
    # ######
    script_run_logger.info("Fetched best model in main script")

    flag = monitor_perf(model, holdout_set_0, threshold=0.15)
    script_run_logger.info(f"Got flag value {flag}")

    # train initially with 0 training, 0 eval, 0 ground truth
    # pass in monitor_perf --> happy

    # pass in monitor_perf with 10 degree ground truth
    # if flag raised (which it will!)
    # train with 0, +10 training, 0, +10 eval, 10 ground truth

    # pass in monitor_perf with -30 degree ground truth
    # if flag raised (which it will!)
    # train with 0, +10, -30 training, 0, +10, -30 eval, -30 ground truth

    # pass in monitor_perf with +20 degree ground truth
    # if flag raised (which it will!)
    # train with 0, +10,+20,+30 -10, -20, -30 (ALL) training, ALL eval, +20 ground truth


if __name__ == "__main__":
    main()
