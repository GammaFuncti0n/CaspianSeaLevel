import yaml
from CaspianLevelSea.data.loader import Loader
from CaspianLevelSea.data.process import ObjectProcessor

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

if __name__=='__main__':
    main()