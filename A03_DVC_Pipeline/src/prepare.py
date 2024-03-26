import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logging_config import a03_logger



def extract_monthly_aggregates(input_files, output_file):
    dfs = []
    for file in input_files:
        df = pd.read_csv(file)
        a03_logger.info(df.head())
        # monthly_agg = df.groupby(pd.Grouper(freq='M')).mean()
        monthly_agg_cols = [i for i in df.columns if i.startswith('Monthly')]
        df = df[['DATE'] + monthly_agg_cols]
        print(df.info())

        # dfs.append(monthly_agg)
        
    # combined_df = pd.concat(dfs)
    # combined_df.to_csv(output_file, index=True)

if __name__ == "__main__":
    input_dir = "data/raw"
    # output_file = "data/processed/ground_truth.csv"
    output_file = "outputs/processed/ground_truth.csv"
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".csv")]

    a03_logger.info(f'input files are {input_files}')
    extract_monthly_aggregates(input_files, output_file)