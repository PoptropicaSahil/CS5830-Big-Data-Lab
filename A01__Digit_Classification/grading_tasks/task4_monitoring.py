import torch
import torch.nn.functional as F
from grading_tasks.task3_train import CustomDataset
from torch.utils.data import DataLoader
from utils.logging_config import script_run_logger


def monitor_perf(model, ground_truth_dataset: tuple, threshold=0.30):
    """Monitor the performance of the given model using the ground truth dataset"""

    batch_size = 64
    images, targets, angles = ground_truth_dataset

    dataset = CustomDataset(images, targets, angles)
    data_loader = DataLoader(dataset, batch_size=batch_size * 2, shuffle=True)

    test_loss = 0
    correct = 0
    total = 0

    model.eval()
    for batch_idx, (data, target, angle) in enumerate(data_loader):
        data, target, _ = data, target, angle
        output = model(data)
        test_loss += F.nll_loss(
            output, target.type(torch.LongTensor)
        ).item()  # sum up batch loss
        pred = output.argmax(
            dim=1, keepdim=True
        )  # get the index of the max log-probability
        correct += pred.eq(target.view_as(pred)).sum().item()
        total += target.size(0)

        if batch_idx % 100 == 0:
            script_run_logger.info(
                f"Ground truth Epoch: [{batch_idx}/{ len(data_loader)} ({100. * batch_idx / len(data_loader):.2f}%)]"
            )

    test_loss /= len(data_loader)
    script_run_logger.info(
        f"Ground truth dataset: Average loss: {test_loss:.4f}, Accuracy: {correct}/{total} ({100*correct/total:.2f}%)\n"
    )

    # if the accumulated error E = |ground_truth_dataset.Y – yhat|>threshold
    # raise a flag!
    flag = 0
    if test_loss > threshold:
        flag = 1
        script_run_logger.warning(
            f"Test loss ({test_loss:.4f}) is higher than threshold {threshold}!"
        )
    else:
        script_run_logger.warning(
            f"Test loss ({test_loss:.4f}) is lower than threshold {threshold}!"
        )

    return flag
