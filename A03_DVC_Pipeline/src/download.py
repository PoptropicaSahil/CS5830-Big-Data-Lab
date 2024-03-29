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
import yaml

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
    a03_logger.info(f'Fetching data for the year {year}, may take time ...')
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
    # Check 10x the required files for non-missing monthly aggregate files 
    # because there are a lot of files (and slow process) if done one-by-one
    num_files_to_read = n_locs * 2 #########
    download_urls = download_urls[::-1][:num_files_to_read]
    

    useful_urls  = []

    def download_file(url):
        nonlocal useful_urls
        monthly_agg_cols = ['MonthlyMeanTemperature']   
        date_col = ['DATE']
        useful_agg_cols = date_col + monthly_agg_cols
        df = pd.read_csv(url, usecols=useful_agg_cols)

        # Check if the length of useful_urls exceeds n_locs
        if len(useful_urls) > n_locs:
            raise Exception("Enough URLs found, stopping the execution.")

        # Only download file if all 12 rows monthly aggregate rows are present
        if df['MonthlyMeanTemperature'].count() == 12:
            useful_urls.append(url)
            a03_logger.info(f'USEFUL CSV DATA found for {url}')
        else:
            a03_logger.debug(f'Unusable CSV DATA at {url}, skipping ...')


    # Call the download_file function and collect the list of URLs
    # try:
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         executor.map(download_file, download_urls)
    # except Exception as e:
    #     a03_logger.info(f"Stopping downloading: {str(e)}")
    
    
    a03_logger.info(f'Number of useful_urls found is {len(useful_urls)}')
    a03_logger.info(f'useful_urls found is {useful_urls}')

    # useful_urls = ['https://www.ncei.noaa.gov/data/local-climatological-data/access/2012/A0000953862.csv', 
    #                ]

    # Step 5: Download the selected files to the data directory
    for url in useful_urls:
        csv_name = url.split("/")[-1]
        filename = os.path.join(data_dir, csv_name)
        wget.download(url, filename)
        a03_logger.info(f'downloading file {filename} to {data_dir} ...')

    # Check if there are enough files in the directory
    file_list = glob.glob(data_dir + '/*')
    if len(file_list) >= n_locs:
        a03_logger.info(f"Success! Files have been downloaded in the {data_dir} directory")
    else:
        a03_logger.info(f"Could not download enough non-missing files, switching to the default data...")
        # copy contents of default directory to raw data directory
        shutil.rmtree(data_dir)
        shutil.copytree("data/default", data_dir)



if __name__ == "__main__":
    
    # Read the params from the params.yaml file as given in
    # https://github.com/iterative/example-get-started/blob/main/src/prepare.py#L41
    params = yaml.safe_load(open("params.yaml"))
    a03_logger.info(f'params are {params}')
    year = params['year']
    n_locs = params['n_locs']

    data_dir = "data/raw"
    # download_data(year=2016, n_locs=1, data_dir=data_dir)
    download_data(year, n_locs, data_dir=data_dir)