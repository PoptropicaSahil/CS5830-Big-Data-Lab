import os
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from grading_tasks.task3_train import CustomDataset
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from torch.utils.data import DataLoader
from utils.logging_config import script_run_logger


def generate_preds(model, data):
    """Generate predictions using the given model and data"""

    batch_size = 64
    images, targets, angles = data

    dataset = CustomDataset(images, targets, angles)
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    all_targets = []
    all_predictions = []

    model.eval()
    for batch_idx, (data, target, angle) in enumerate(data_loader):
        data, target, _ = data, target, angle
        output = model(data)
        pred = output.argmax(dim=1, keepdim=True)
        all_targets.append(target.numpy())
        all_predictions.append(pred.squeeze().numpy())

    all_targets = np.concatenate(all_targets)
    all_predictions = np.concatenate(all_predictions)

    return all_targets, all_predictions


def show_model_predictions(targets, predictions, labels, model_saving_path):
    """
    Calculate metrics for each class and save the results to a CSV file.
    Display performance metrics in a bar chart and return the results.
    """
    script_run_logger.info("show_model_predictions")

    accuracy = []
    recall = []
    precision = []
    f1 = []

    for label in labels:
        y_true_label = np.array(targets) == label
        y_pred_label = np.array(predictions) == label
        accuracy.append(accuracy_score(y_true_label, y_pred_label))
        recall.append(recall_score(y_true_label, y_pred_label))
        precision.append(precision_score(y_true_label, y_pred_label))
        f1.append(f1_score(y_true_label, y_pred_label))

    # Save results to a CSV file
    results = pd.DataFrame(
        {
            "Class": labels,
            "Accuracy": accuracy,
            "Recall": recall,
            "Precision": precision,
            "F1": f1,
        }
    )
    results = results.round(2)  # round-off
    results.to_csv(f"{model_saving_path}performance_metrics.csv", index=False)

    # make the figure
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    for ax in axs.flat:
        ax.set_xticks(range(10))
        ax.set_xticklabels(range(10))
        ax.set_xlabel("Classes")

    plt.title("Performance Metrics")

    axs[0, 0].bar(results["Class"], results["Accuracy"])
    axs[0, 0].set_title("Accuracy")

    axs[0, 1].bar(results["Class"], results["Recall"])
    axs[0, 1].set_title("Recall")

    axs[1, 0].bar(results["Class"], results["Precision"])
    axs[1, 0].set_title("Precision")

    axs[1, 1].bar(results["Class"], results["F1"])
    axs[1, 1].set_title("F1 Score")
    fig.tight_layout()
    plt.savefig(f"{model_saving_path}performance_metrics.png", bbox_inches="tight")
    plt.show()

    return results


def show_confusion_matrix(targets, predictions, labels, model_saving_path, note=None):
    """Display confusion matrix and save it to a file"""
    conf_mat = confusion_matrix(targets, predictions, labels=labels, normalize=None)

    df_cm = pd.DataFrame(conf_mat, index=labels, columns=labels)
    plt.figure(figsize=(10, 10))
    plt.title(f"Normalised Confusion Matrix (5000 samples)\n {note}")
    sns.heatmap(df_cm, annot=True, fmt="d")
    plt.xlabel("Actuals")
    plt.ylabel("Predictions")
    plt.savefig(f"{model_saving_path}confusion_matrix.png", bbox_inches="tight")
    plt.show()
    return


def generate_performance_metrics(model, data):
    """Generate performance metrics for the given model and data by the helper functions defined above"""

    # check if performance metrics directory exists
    model_saving_path = "./performance_metrics/"
    if not os.path.exists(model_saving_path):
        script_run_logger.info(
            f"Existing metrics directory not found, creating: {model_saving_path}"
        )
        os.makedirs(model_saving_path)
    else:
        # clear contents of the dir if it already exists
        script_run_logger.info(
            f"Existing metrics directory found, clearing contents {model_saving_path}"
        )
        shutil.rmtree(model_saving_path)
        os.makedirs(model_saving_path)

    targets, predictions = generate_preds(model, data)
    labels = range(10)

    results = show_model_predictions(targets, predictions, labels, model_saving_path)

    mean_accuracy = results["Accuracy"].mean()
    note = f"Mean Accuracy: {mean_accuracy:.2f}"
    show_confusion_matrix(targets, predictions, labels, model_saving_path, note=note)

    return
