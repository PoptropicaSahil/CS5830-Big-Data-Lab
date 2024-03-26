import os
import wget
import requests
from bs4 import BeautifulSoup
import random
import sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logging_config import a03_logger




def download_data(year, n_locs, data_dir):

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
    links = soup.find_all('a', href=True, attrs={'href': lambda href: href.endswith('.csv')})

    # Step 3: Select the desired number of files
    selected_links = random.sample(links, n_locs)
    # selected_links = links[-num_files_to_download:]
    download_urls = [url + link['href'] for link in selected_links]
    a03_logger.info(f'download_urls are {download_urls}' )
    
    # Step 4: Download the selected files
    for idx, link in enumerate(download_urls):
        csv_name = link.split("/")[-1]
        filename = os.path.join(data_dir, csv_name)
        wget.download(link, filename)

    a03_logger.info(f'downloaded the files')


if __name__ == "__main__":
    # Replace with your actual data source URL
    data_dir = "data/raw"
    download_data(year=1960, n_locs=3, data_dir=data_dir)