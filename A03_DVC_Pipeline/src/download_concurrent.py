import os
import wget
import requests
from bs4 import BeautifulSoup
import random
import sys
import shutil
import concurrent.futures
import threading
import pandas as pd
import time
import re
import glob

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logging_config import a03_logger

downloaded_files_counter = 0
counter_lock = threading.Lock()

def download_data(year, n_locs, data_dir):
    """
    Downloads data from a specified year and location.
    Uses concurrent for parallel processing
    """
    
    # Step 0: Clear the data directory 
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    
    os.makedirs(data_dir, exist_ok=True)

    a03_logger.info(f'cleared the data directory {data_dir}')

    # Step 1: Fetch the HTML content
    a03_logger.info(f'Fetching data for the year {year}')
    url = f"https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}/"
    response = requests.get(url)
    html_content = response.text
    
    # Step 2: Parse the HTML and extract links
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    csv_hrefs = [link['href'] for link in links if re.match(r".+\.csv$", link['href'])]


    # Step 3: Select the desired number of files
    download_urls = [url + csv_name for csv_name in csv_hrefs]
    a03_logger.info(f'Few download_urls on the page are {download_urls[:5]}' )
    
    
    # Step 4: Download the selected files
    # If we have enough number of files from this year and n_loc available then continue
    # Else work with default files

    # Check 10x the required files for non-missing monthly aggregate files 
    # because there are a lot of files (and slow process) if done one-by-one
    num_files_to_read = n_locs * 20 
    download_urls = download_urls[::-1][:num_files_to_read]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda url: download_file(url, data_dir, n_locs), download_urls)


    # Check if there are enough files in the directory
    file_list = glob.glob(data_dir + '/*')
    if len(file_list) == n_locs:
        a03_logger.info(f"Success! Exactly {n_locs} files have been downloaded in the {data_dir} directory")
    else:
        a03_logger.warning(f"Could not download enough non-missing files, switching to the default data...")
        


def download_file(url, data_dir, n_locs):

    global downloaded_files_counter

    with counter_lock:
        if downloaded_files_counter >= n_locs:
            a03_logger.debug(f'Have downloaded the required number of files, continuing...')
            return  # Skip further downloads


    # only download those files which have all 12 monthly aggregate rows present, non-null
    # we only work with the temperature field
    
    # Daily aggregate fields 
    # daily_agg_cols = ['DailyAverageDewPointTemperature', 'DailyAverageDryBulbTemperature', 'DailyAverageWetBulbTemperature']
        
    # Monthly aggregate fields:
    monthly_agg_cols = ['MonthlyMeanTemperature']
        
    # useful_agg_cols = daily_agg_cols + monthly_agg_cols

    # Date fields:
    date_col = ['DATE']
    useful_agg_cols = date_col + monthly_agg_cols
    df = pd.read_csv(url, usecols=useful_agg_cols)

    # Only download file if all 12 rows monthly aggreate rows are present
    if df['MonthlyMeanTemperature'].count() == 12:
        with counter_lock:
            downloaded_files_counter += 1

        a03_logger.info(f'USEFUL CSV DATA found for {url}')
        csv_name = url.split("/")[-1]
        filename = os.path.join(data_dir, csv_name)
        wget.download(url, filename)

    else:
        a03_logger.debug(f'Unusable CSV DATA at {url}, skipping ...')
       



if __name__ == "__main__":
    # Replace with your actual data source URL
    data_dir = "data/raw"
    download_data(year=2014, n_locs=3, data_dir=data_dir)