import sys
import os
import pandas as pd # type: ignore
import numpy as np # type: ignore
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
 
from sklearn.compose import ColumnTransformer # type: ignore
from sklearn.preprocessing import StandardScaler, OneHotEncoder # type: ignore
from sklearn.pipeline import Pipeline # type: ignore
from src.utils.common import save_object # type: ignore
from sklearn.impute import SimpleImputer # type: ignore

@dataclass
class DataTransformationConfig:
    '''Configuration for data transformation paths.'''
    preprocessor_obj_file_path: str = os.path.join("artifacts", "models", "preprocessor.joblib")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_transformation_object(self):
        try:
            mean_inpute_cols = ['loan_int_rate']
            median_inpute_cols = ['person_age','person_income','person_emp_length','loan_amnt','loan_percent_income','cb_person_cred_hist_length']
            categorical_cols = ['person_home_ownership','loan_grade','cb_person_default_on_file','loan_intent',]
            
            mean_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])
            median_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            categorical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder(drop='first', handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))
            ])
            logging.info("Creating column transformer for data transformation.")
            logging.info(f"Mean Imputation columns: {mean_inpute_cols}")
            logging.info(f"Median Imputation columns: {median_inpute_cols}")
            logging.info(f"Categorical columns: {categorical_cols}")
            
            logging.info("Defining preprocessing object.")
            preprocessor = ColumnTransformer(transformers=[
                ('mean_pipeline', mean_pipeline, mean_inpute_cols),
                ('median_pipeline', median_pipeline, median_inpute_cols),
                ('categorical_pipeline', categorical_pipeline, categorical_cols)
            ], remainder='passthrough')
            
            return preprocessor
            
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path: str, test_path: str):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Read train and test data completed.")
            logging.info("Obtaining preprocessing object.")
            preprocessing_obj = self.get_transformation_object()
            
            target_column_name = 'loan_status'
            
            # Splitting input and target feature from training and testing dataframe
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info("Applying preprocessing object on training and testing data.")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            logging.info("Concatenating processed input features and target feature.")
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            logging.info("Saving preprocessing object.")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)
            