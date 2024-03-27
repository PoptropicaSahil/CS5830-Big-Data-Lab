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




# LOGIC LOOOOOOOP
# import concurrent.futures
# import threading
# import pandas as pd
# import time


# useful_df = []
# n_locs = 2
# lock = threading.Lock()

# # Define the download_urls
# files_read = 0  # Initialize files_read

# def process_url(url):
#     global files_read

#     cols_to_read = ['MonthlyAverageRH', 'MonthlyDewpointTemperature', 'MonthlyMeanTemperature',
#                     'MonthlySeaLevelPressure', 'MonthlyStationPressure', 'MonthlyTotalLiquidPrecipitation',
#                     'MonthlyTotalSnowfall','MonthlyWetBulb']

#     df = pd.read_csv(url, usecols = cols_to_read)
#     # monthly_agg_cols = [i for i in df.columns if i.startswith('Monthly')]
#     # df_agg = df[monthly_agg_cols]

#     # df_agg = df.copy()

#     with lock:
#         files_read += 1
#         print(f'Read {files_read} csv', flush=True)

#     if df.isnull().all().all(): # df_agg
#         print(f'not useful df {url}')
#     else:
#         useful_df.append(url)
#         print(f'***** useful df found for {url}')
        
#         with lock:
#             if len(useful_df) == n_locs:
#                 print('Found enough URLs, breaking...')
#                 return False
            
#     return True

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     num_files_to_read = n_locs * 10
#     executor.map(process_url, download_urls[::-1][:num_files_to_read])