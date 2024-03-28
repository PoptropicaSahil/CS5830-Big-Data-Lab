import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logging_config import a03_logger


def extract_monthly_aggregates(input_files, output_file):
    ground_truths = []
    for file in input_files:
        a03_logger.info(f'extracting monthly aggregate of {file}')
        
        # a03_logger.info(df.head())
        # monthly_agg = df.groupby(pd.Grouper(freq='M')).mean()
        monthly_agg_cols = ['MonthlyMeanTemperature']  # MonthlyDewpointTemperature
        # df = df[['DATE'] + monthly_agg_cols]
        date_cols = ['DATE']

        useful_cols = monthly_agg_cols + date_cols
        df = pd.read_csv(file,  usecols=useful_cols)

        df = df[df['MonthlyMeanTemperature'].notnull()]

        avg = df['MonthlyMeanTemperature']
        # a03_logger.info(avg)

        ground_truths.append(avg)
        
    combined_df = pd.concat(ground_truths)
    combined_df.reset_index(drop=True).to_csv(output_file, index=True)
    a03_logger.info(f'Saved combined aggregates to {output_file}')

if __name__ == "__main__":
    input_dir = "data/raw"
    input_dir = "data/default"
    # output_file = "data/processed/ground_truth.csv"
    output_file = "outputs/processed/ground_truth.csv"
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".csv")]

    a03_logger.info(f'input files are {input_files}')
    extract_monthly_aggregates(input_files, output_file)

