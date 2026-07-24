import yaml
import logging
from src.data.loader import Loader
from src.data.process import ObjectProcessor

logging.basicConfig(
    level=logging.DEBUG, 
    filename="log.log", 
    filemode="w", 
    format="%(asctime)s %(levelname)s %(message)s", 
    encoding='utf-8'
    )

def main():
    with open('configs/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    loader = Loader(config['data']['url_link'])
    loader.load(config['data']['raw_data_path'])

    processor = ObjectProcessor()
    processor.process_object(
        config['data']['raw_data_path'], 
        config['data']['object_path'], 
        config['data']['metadata_path']
        )
    processor.process_data(
        config['data']['object_path'], 
        config['data']['metadata_path'],
        config['data']['data_path']
        )

if __name__=='__main__':
    main()