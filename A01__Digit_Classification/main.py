# main_script.py
import argparse

from load_data import load_mnist_data

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

    data_loader = load_mnist_data(save_path=args.data_dir)
    train_data, test_data = data_loader.get_datasets()
    
    # Show few images from training data 
    # data_loader.plot_images(train_data)

    script_run_logger.info("MNIST dataset loaded successfully.")

    var_chk_logger.debug(f"image and labels are {[(type(image), type(label)) for image, label in train_data][:3]}")

    # Train classifier
    # train_classifier(train_data, test_data, args.epochs, args.batch_size, args.learning_rate)


if __name__ == "__main__":
    main()
