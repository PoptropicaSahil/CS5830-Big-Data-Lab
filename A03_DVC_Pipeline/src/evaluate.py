import pandas as pd
from sklearn.metrics import r2_score

import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logging_config import a03_logger


def evaluate_consistency(ground_truth_file, computed_file):
    ground_truth = pd.read_csv(ground_truth_file, index_col=0)
    computed = pd.read_csv(computed_file, index_col=0)
    
    r2 = r2_score(ground_truth, computed)
    a03_logger.info(f"R^2 score: {r2}")
    
    if r2 >= 0.9:
        a03_logger.info("Consistent (C)")
    else:
        a03_logger.info("Not consistent")

if __name__ == "__main__":
    ground_truth_file = "outputs/processed/ground_truth.csv"
    computed_file = "outputs/processed/computed_aggregates.csv"
    evaluate_consistency(ground_truth_file, computed_file)