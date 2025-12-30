import sys
import os
import yaml # type: ignore
import joblib # type: ignore
from src.logger import logging
from src.exception import CustomException
from ensure import ensure_annotations # type: ignore
from box import ConfigBox # type: ignore
from pathlib import Path

def read_yaml(file_path: Path) -> ConfigBox:
    '''Reads a YAML file and returns its contents as a ConfigBox object.'''
    try:
        with open(file_path, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"YAML file: {file_path} loaded successfully")
            return ConfigBox(content)
    except Exception as e:
        raise CustomException(e, sys)

def create_directories(path_to_directories: list, verbose=True):
    '''Creates directories from the given list of paths.'''
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logging.info(f"Directory created at: {path}")
    except Exception as e:
        raise CustomException(e, sys)

def save_object(file_path, obj):
    '''Saves a Python object to a file using joblib.'''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            joblib.dump(obj, file_obj)
            logging.info(f"Object saved successfully at: {file_path}")
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    '''Loads a Python object from a file using joblib.'''
    try:
        if not os.path.exists(file_path):
            raise CustomException(f"The file: {file_path} does not exist", sys)
        with open(file_path, 'rb') as file_obj:
            obj = joblib.load(file_obj)
            logging.info(f"Object loaded successfully from: {file_path}")
            return obj
    except Exception as e:
        raise CustomException(e, sys)