import re
import pandas as pd
import sqlite3
import zipfile
import io
import os
import logging

logging.basicConfig(
    level=logging.INFO, 
    filename="log.log", 
    filemode="w", 
    format="%(asctime)s %(levelname)s %(message)s", 
    encoding='utf-8'
    )

class ObjectProcessor():
    '''
    Class for process raw data to the database
    '''
    def __init__(self):
        '''
        Init class for ObjectProcess
        '''
        self.metadata_df = []
        self.metadata_patterns = {
            'post_name': re.compile(r'post[^_]*_+([^_]+)_+$'),
            'opening_date': re.compile(r'opening date[^_]*_+([^_]+)_+$'),
            'latitude': re.compile(r'latitude[^_]*_+([^_]+)_+'),
            'longitude': re.compile(r'longitude[^_]*_+([^_]+)_+'),
            'post_datum': re.compile(r'post datum[^_]*_+([^_]+)_+'),
            'altitude_system': re.compile(r'(?:altitude system[^_]*_+|from the)([^_]+)' ) # r'altitude system[^_]*_+([^_]+)_+' # r'(?:altitude system[^_]*_+|from the)([^_]+)' 
        }
        self.year_pattern = re.compile(r'^\d{4,}$')

    def process_object(self, raw_data_path: str, object_path: str, metadata_path: str) -> None:
        '''
        Method for process every post, parse metadata and level sea
        :params:
            raw_data_path: str - path to raw zip file with posts
            object_path: str - path to object storage where save data
            metadata_path: str - path to metadata storage
        '''
        # Make connection to sqlite server
        self.conn = sqlite3.connect(object_path)

        # Read data
        with zipfile.ZipFile(raw_data_path, 'r') as self.zf:
            xls_files = [f for f in self.zf.namelist() if f.endswith(('.xls', '.xlsx'))]

            # iterate over posts in zip
            for file_name in xls_files:
                self._process_file(file_name)

            pd.DataFrame(self.metadata_df).to_csv(metadata_path, index=False)
        self.conn.close()
    
    def process_data(self, object_path: str, metadata_path: str, data_path: str) -> None:
        '''
        Method for process raw data (objects) and save in data_path
        :params:
            object_path: str - path to object storage where load data
            metadata_path: str - path with metadata storage
            data_path: str - path where contain proocessed data 
        '''
        # Load metadata and zero-level
        metadata_df = pd.read_csv(metadata_path)

        # Make connection to sqlite server
        self.conn = sqlite3.connect(object_path)

        # Process data
        os.makedirs(data_path, exist_ok=True)
        post_names = pd.read_sql("SELECT name FROM sqlite_master", self.conn)['name']
        for post_name in post_names:
            df = pd.read_sql(f"SELECT * FROM {post_name}", self.conn)
            zero_level = metadata_df[metadata_df['post_file']==post_name]['post_datum'].values[0]
            logging.debug(f"{post_name} zero level: {zero_level}")
            zero_level = -float(str(zero_level).replace(',', '.').replace('-', ''))
            
            df['sea_level'] = pd.to_numeric(df['sea_level'], errors='coerce')/100 + zero_level
            df.to_csv(os.path.join(data_path, f"{post_name}.csv"))
            logging.info(f"Succesfully save dataframe: {post_name}.csv")
        self.conn.close()
    
    def _process_file(self, file_name) -> None:
        '''
        Method for process one file (post) and save result in database
        '''
        post_file = self._get_post_name(file_name)
        meta_info = {key: None for key in self.metadata_patterns}
        meta_info['post_file'] = post_file

        # Open file
        with self.zf.open(file_name) as zip_file:
            df = pd.read_excel(io.BytesIO(zip_file.read()), header=None)
        
        df_ = pd.DataFrame(columns=['datetime', 'sea_level'])
        current_index = 0
        # Iterate over dataframe: parse metadata and data
        for i in range(len(df)):
            s_lower = str(df.iloc[i,0]).strip().lower()
            for key, pattern in self.metadata_patterns.items():
                if meta_info[key] is None:
                    match = pattern.search(s_lower)
                    if match:
                        meta_info[key] = match.group(1)
            
            match = re.search(self.year_pattern, s_lower)
            if match: 
                year = df.iloc[i,0]
                for month in range(1,13):
                    df_.loc[current_index,'datetime'] = f'{month}-{year}'
                    df_.loc[current_index,'sea_level'] = df.iloc[i,month]
                    current_index += 1
        
        self.metadata_df.append(meta_info)
        df_.to_sql(name=post_file, con=self.conn, if_exists='replace', index=False)

        logging.info(f"Succesfully save post: {post_file}")

    def _get_post_name(self, file_name: str) -> str:
        '''
        Method for extract name of post from the file name.
        For example:
        'Sea-level-EN/AVERAGE/TUL_av.xls' -> 'TUL'

        First search lettres before '_av.'
        After filter symbols ['(', ')', ' '] and shange them on ''

        :params:
            file_name: str - path to the file
        :returns:
            post_name: str - name of the post
        '''
        # Find lettres before '_av.'
        name_pattern = r'[A-Za-z0-9_\(\) ]+(?=_av\.)'
        post_name = re.findall(name_pattern, file_name)[-1]

        # Filter symbols ['(', ')', ' ']
        special_symbols_pattern = r'[\(\)\s]'
        post_name = re.sub(special_symbols_pattern, '', post_name)

        return post_name