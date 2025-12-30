from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging
import sys

if __name__ == "__main__":
    try:
        ingestion = DataIngestion()
        train_data_path, test_data_path = ingestion.initiate_data_ingestion()
        
        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
        
        model_trainer = ModelTrainer()
        f1_score = model_trainer.initiate_model_trainer(train_arr, test_arr)
        
        print(f"Model training completed with F1 Score: {f1_score}")
        logging.info(f"Model training completed with F1 Score: {f1_score}")
    except Exception as e:
        logging.error(f"An error occurred in the main pipeline: {str(e)}.")
        raise e