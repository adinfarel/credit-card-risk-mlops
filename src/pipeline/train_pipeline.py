import sys
import os
from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


class TrainPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()
    
    def run_pipeline(self):
        try:
            logging.info("Starting End-to-End Training Pipeline")
            
            # Ingestion data
            train_path, test_path = self.data_ingestion.initiate_data_ingestion()
            
            # Transform data
            train_arr, test_arr, preprocessor_file_path = self.data_transformation.initiate_data_transformation(train_path, test_path)
            
            # Train model
            model_score = self.model_trainer.initiate_model_trainer(train_arr, test_arr)
            
            logging.info(f"Training Pipeline Completed. Best Model Scores: {model_score}")
            
            return model_score
        
        except Exception as e:
            raise CustomException(e, sys)
    
if __name__ == "__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
            
            