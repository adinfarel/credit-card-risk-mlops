import sys
import os
from src.logger import logging
from src.exception import CustomException
import pandas as pd # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    '''Configuration for data ingestion paths.'''
    raw_data_path: str = os.path.join("artifacts", "data", "interim", "credit_risk_dataset_clean.csv")
    train_data_path: str = os.path.join("artifacts", "data", "processed", "train.csv")
    test_data_path: str = os.path.join("artifacts", "data", "processed", "test.csv")
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logging.info("Starting data ingestion process.")
        try:
            df = pd.read_csv(self.ingestion_config.raw_data_path)
            logging.info(f"Dataset read successfully: {self.ingestion_config.raw_data_path}.")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            logging.info("Splitting dataset into train and test sets.")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)
            
            logging.info("Data ingestion completed successfully.")
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)