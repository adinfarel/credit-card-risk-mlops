import sys
import pandas as pd # type: ignore
from src.exception import CustomException
from src.logger import logging
from src.utils.common import load_object

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features):
        try:
            logging.info("Loading preprocessor and model for prediction.")
            preprocessor_path = "artifacts/models/preprocessor.joblib"
            model_path = "artifacts/models/model.joblib"
            
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)
            
            logging.info("Transforming input features using the preprocessor.")
            data_scaled = preprocessor.transform(features)
            
            logging.info("Making predictions using the trained model.")
            preds = model.predict(data_scaled)
            
            return preds
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    '''Mapping input features for prediction.'''
    def __init__(self, person_age, person_income, person_home_ownership, 
                 person_emp_length, loan_intent, loan_grade, loan_amnt, 
                 loan_int_rate, cb_person_default_on_file, 
                 loan_percent_income, cb_person_cred_hist_length):
        self.person_age = person_age
        self.person_income = person_income
        self.person_home_ownership = person_home_ownership
        self.person_emp_length = person_emp_length
        self.loan_intent = loan_intent
        self.loan_grade = loan_grade
        self.loan_amnt = loan_amnt
        self.loan_int_rate = loan_int_rate
        self.cb_person_default_on_file = cb_person_default_on_file
        self.loan_percent_income = loan_percent_income
        self.cb_person_cred_hist_length = cb_person_cred_hist_length
    
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "person_age": [self.person_age],
                "person_income": [self.person_income],
                "person_home_ownership": [self.person_home_ownership],
                "person_emp_length": [self.person_emp_length],
                "loan_intent": [self.loan_intent],
                "loan_grade": [self.loan_grade],
                "loan_amnt": [self.loan_amnt],
                "loan_int_rate": [self.loan_int_rate],
                "cb_person_default_on_file": [self.cb_person_default_on_file],
                "loan_percent_income": [self.loan_percent_income],
                "cb_person_cred_hist_length": [self.cb_person_cred_hist_length]
            }
            
            logging.info("Converting input data to DataFrame.")
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)