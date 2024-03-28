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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logging_config import a03_logger

def download_data(year, n_locs, data_dir):
	# """
	# Downloads data from a specified year and location.
    # Uses concurrent for parallel processing
	# """
    
    # Step 0: Clear the data directory 
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    
    os.makedirs(data_dir, exist_ok=True)
    a03_logger.info(f'cleared the data directory {data_dir}')

    # Step 1: Fetch the HTML content
    url = f"https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}/"
    response = requests.get(url)
    html_content = response.text
    
    # Step 2: Parse the HTML and extract links
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    csv_hrefs = [link['href'] for link in links if re.match(r".+\.csv$", link['href'])]


    # Step 3: Select the desired number of files
    # selected_links = random.sample(links, n_locs)
    # selected_links = links[-num_files_to_download:]
    # download_urls = [url + link['href'] for link in links]
    download_urls = [url + csv_name for csv_name in csv_hrefs]
    a03_logger.info(f'Few download_urls on the page are {download_urls[:5]}' )
    
    
    # Step 4: Download the selected files
    # If we have enough number of files from this year and n_loc available then continue
    # Else work with default files
    
    num_files_to_read = n_locs * 10 
    download_urls = download_urls[::-1][:num_files_to_read]

    monthly_agg_cols = ['MonthlyAverageRH', 'MonthlyDewpointTemperature', 'MonthlyMeanTemperature',
                        'MonthlySeaLevelPressure', 'MonthlyStationPressure', 'MonthlyTotalLiquidPrecipitation',
                        'MonthlyTotalSnowfall','MonthlyWetBulb']
    
    useful_urls = 0

    for idx, url in enumerate(download_urls):
        df = pd.read_csv(url, usecols = monthly_agg_cols)
        if df.isnull().all().all(): 
            a03_logger.debug(f'Fully missing monthly values at {url}')
        else:
            # useful_df.append(url)
            a03_logger.debug(f'**USEFUL** CSV DATA found for {url}')
            csv_name = url.split("/")[-1]
            filename = os.path.join(data_dir, csv_name)
            wget.download(url, filename)
            useful_urls += 1

        if useful_urls == n_locs:
            break



    # If the monthly aggregate values are all nulls then we skip

    a03_logger.info(f'downloaded the files')


if __name__ == "__main__":
    # Replace with your actual data source URL
    data_dir = "data/raw"
    download_data(year=2012, n_locs=3, data_dir=data_dir)