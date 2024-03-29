import os
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logging_config import a03_logger


def compute_monthly_aggregates(input_files, output_file, fields):
    aggregates = []
    for file in input_files:
        a03_logger.info(f'computing monthly aggregate of {file}')
        
        monthly_agg_cols = ['MonthlyMeanTemperature']  # MonthlyDewpointTemperature
        daily_agg_cols = 'DailyAverageDryBulbTemperature'
        date_cols = 'DATE'

        useful_cols = [daily_agg_cols] + [date_cols]
        df = pd.read_csv(file,  usecols=useful_cols)
        df[date_cols] = pd.to_datetime(df[date_cols])  # Ensure the 'DATE' column is in datetime format

        # Some files have the Daily readings as
        # 24, 20s, 24 ...
        # So we just extract the numbers
        # explicitly convert the column to a string type at first
        df[daily_agg_cols] = df[daily_agg_cols].astype(str)
        df[daily_agg_cols] = df[daily_agg_cols].str.extract('(\d+)').astype(float)


        # Group by month and calculate the mean temperature
        monthly_averages = df.groupby(df['DATE'].dt.month)[daily_agg_cols].mean()
        aggregates.append(monthly_averages)

        
    combined_df = pd.concat(aggregates)
    combined_df.reset_index(drop=True).to_csv(output_file, index=True)
    a03_logger.info(f'Saved computed aggregates to {output_file}')

if __name__ == "__main__":
    input_dir = "data/raw"
    output_file = "outputs/processed/computed_aggregates.csv"
    fields = ["DryBulbTemperature", "Precipitation", "RelativeHumidity"]
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".csv")]
    compute_monthly_aggregates(input_files, output_file, fields)