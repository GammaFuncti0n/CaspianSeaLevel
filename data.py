import logging
import requests
from bs4 import BeautifulSoup
import yaml
import os

logging.basicConfig(
    level=logging.INFO, 
    filename="requests.log", 
    filemode="w", 
    format="%(asctime)s %(levelname)s %(message)s", 
    encoding='utf-8'
    )

def main() -> None:
    # load config
    with open('configs/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    logging.info(config)
    
    parent_url = config['data']['url_link']
    data_url = get_data_url(parent_url)
    load_data(data_url=data_url, data_path=config['data']['path'], chunk_size=8192)

def get_data_url(parent_url: str) -> str:
    '''
    Get url for actual level sea data from the parent page
    :params:
        parent_url: str - url for parent page where find data
    :returns:
        data_url: str - url where contain data
    '''
    try:
        response = requests.get(parent_url)
        response.raise_for_status()

        logging.debug(response.text)
        data_url = find_data_url(response.text)

    except requests.exceptions.RequestException as e:
        logging.critical(f"Fatal error: {e}")
    
    return data_url

def find_data_url(response_text: str) -> str:
    '''
    Based on the response from the sea site, find the url for actual data
    :params:
        response_text: str - the text response from the site
    :returns:
        data_url: str - url for actual data level sea
    '''
    soup = BeautifulSoup(response_text, 'html.parser')
    link_tag = soup.find('a', href=lambda href: href and 'Sea-level-EN.zip' in href)

    # check on existance pf attribute and get link
    if link_tag:
        data_url = link_tag.get('href')
        logging.info(f"Url for data: {data_url}") 
    else:
        data_url = None
        logging.error(f"URL on Sea-level-EN.zip not found")
    
    return data_url

def load_data(data_url: str, data_path: str, chunk_size: int=8192) -> None:
    '''
    Load data from data_path
    :params:
        data_url: str - url link on data of level sea
        data_path: str - path where load data
        chunk_size: int default(8192) - the size of data chunk 
    '''
    os.makedirs(data_path, exist_ok=True)
    try:
        response = requests.get(data_url, stream=True, timeout=30)
        response.raise_for_status()

        with open(os.path.join(data_path, 'level_sea.zip'), 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
        
        logging.info(f"Level sea data succsesfully loaded in {os.path.join(data_path, 'level_sea.zip')}")
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during loading data: {e}")

if __name__=='__main__':
    main()