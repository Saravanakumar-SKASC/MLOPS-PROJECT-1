import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config
        self.bucket_name = self.config["data_ingestion"]["bucket_name"]
        self.file_name = self.config["data_ingestion"]["bucket_file_name"]
        self.train_ratio = self.config["data_ingestion"]["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(f"Data Ingestion started with {self.bucket_name} and {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\sarav\Downloads\resolute-fold-458114-c1-a781a42b4979.json"
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"File downloaded successfully from {self.bucket_name} and {self.file_name} to {RAW_FILE_PATH}")
        except Exception as e:
            logger.error("Error while downloading file from GCP")
            raise CustomException(f"Failed to download file from GCP: {str(e)}")
        
    def split_data(self):
        
        try:
            logger.info("Splitting data into train and test")
            
            data = pd.read_csv(RAW_FILE_PATH)
           
            train_data, test_data = train_test_split(data, test_size=1-self.train_ratio, random_state=42)
            
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info("Data split successfully")
        except Exception as e:
            logger.error("Error while splitting data")
            raise CustomException(f"Failed to split data: {str(e)}")
        
    def run(self):
        try:
            logger.info("Starting Ingestion process")
            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Ingestion process completed")
        except Exception as ce:
            logger.error(f"Error while running ingestion process :{str(ce)}")
            
        finally:
            logger.info("Data Ingestion process completed")

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    