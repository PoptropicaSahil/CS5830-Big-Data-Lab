# main_script.py
import argparse

from load_data import load_mnist_data

# from train_classifier import train_classifier
from utils.logging_config import script_run_logger, var_chk_logger
# from utils.show_data import plot_image

from grading_tasks.task1_rotate_img import rotate
from grading_tasks.task2_oversample import generate_dataset


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

    data_loader = load_mnist_data(save_path=args.data_dir)
    train_data, test_data = data_loader.get_datasets()

    # Show few images from training data
    # data_loader.plot_images_from_dataloader(train_data)

    script_run_logger.info("MNIST dataset loaded successfully.")
    script_run_logger.info(
        f"Size of train data: {len(train_data)}, test data: {len(test_data)}"
    )

    # var_chk_logger.debug(
    #     f"image and labels are {[(type(image), type(label)) for image, label in train_data][:3]}"
    # )

    rotation_angle = 30
    image, label = train_data[0]

    var_chk_logger.debug(f"image and label are of types {type(image), type(label)}")
    var_chk_logger.debug(f"image size is {image.shape}")

    # plot_image(image, label)

    new_img = rotate(image, angle=rotation_angle)
    # plot_image(new_img, label)

    updated_train_data = generate_dataset(train_data, oversample_rate=8)
    script_run_logger.info(f"Oversampled train data, size = {len(updated_train_data)}")

    updated_test_data = generate_dataset(test_data, oversample_rate=8)
    script_run_logger.info(f"Oversampled test data, size = {len(updated_test_data)}")


if __name__ == "__main__":
    main()
