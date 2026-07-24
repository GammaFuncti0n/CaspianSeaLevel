import logging
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

class Loader():
    '''
    Class for load raw data from the site
    '''
    def __init__(self, parent_url: str, chunk_size: int=8192) -> None:
        '''
        Init class for Loader
        :params:
            parent_url: str - url for parent page where find data
            chunk_size: int (default=8192) - the size of data chunk during loading
        '''
        self.parent_url = parent_url
        self.chunk_size = chunk_size

    def load(self, data_path: str):
        '''
        :params:
            data_path: str - path where load data
        '''
        data_url = self._find_url_link(self.parent_url)
        self.__load(url_link=data_url, data_path=data_path, chunk_size=self.chunk_size)
    
    def _find_url_link(self, parent_url: str) -> str:
        '''
        Get url for actual level sea data from the parent page
        :params:
            parent_url: str - url for parent page where find data
        :returns:
            data_url: str - url where contain data
        '''
        try:
            # try to connect to parent page
            response = requests.get(parent_url, timeout=10)
            response.raise_for_status()
            logging.debug(response.text)
            
            # Find url for data
            soup = BeautifulSoup(response.text, 'html.parser')
            link_tag = soup.find('a', href=lambda href: href and 'Sea-level-EN.zip' in href)
            # check on existance if attribute and get link
            if link_tag:
                data_url = link_tag.get('href')
                logging.info(f"Url for data: {data_url}") 
            else:
                data_url = None
                logging.error(f"URL on Sea-level-EN.zip not found")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error during connection to {parent_url} or during search url: {e}")
        
        return data_url
    
    def __load(self, url_link: str, data_path: str, chunk_size: int) -> None:
        '''
        Load data from url to data_path
        :params:
            url_link: str - url link on data of level sea
            data_path: str - path where save data
            chunk_size: int - the size of data chunk 
        '''
        # create parent directory if not exist
        path = Path(data_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # try to connect and save data
        try:
            response = requests.get(url_link, stream=True, timeout=30)
            response.raise_for_status()

            with open(data_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            
            logging.info(f"Level sea data succsesfully saved in {data_path}")
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during loading data: {e}")


