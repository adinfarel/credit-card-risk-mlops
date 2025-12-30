import os
import sys
from dataclasses import dataclass

import mlflow # type: ignore
import mlflow.sklearn # type: ignore

from src.logger import logging
from src.exception import CustomException
from src.utils.common import save_object

from imblearn.over_sampling import SMOTE # type: ignore
from imblearn.pipeline import Pipeline # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.model_selection import StratifiedKFold, GridSearchCV # type: ignore
from xgboost import XGBClassifier # type: ignore
from lightgbm import LGBMClassifier # type: ignore
from sklearn.metrics import f1_score # type: ignore

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "models", "model.joblib")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info('Splitting training and testing data.')
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            
            models = {
                "LogisticRegression": LogisticRegression(random_state=42, max_iter=1000),
                "XGBClassifier": XGBClassifier(random_state=42, n_jobs=-1),
                "LGBMClassifier": LGBMClassifier(random_state=42, n_jobs=-1, verbose=-1)
            }
            
            params = {
                'LogisticRegression': {
                    'model__C': [0.1, 1, 10],
                    'model__penalty': ['l2'], 
                    'model__solver': ['lbfgs', 'liblinear']
                },
                'XGBClassifier': {
                    'model__learning_rate': [0.01, 0.1],
                    'model__n_estimators': [100, 200],
                    'model__max_depth': [3, 5, 7],
                    'model__subsample': [0.8, 1.0], 
                    'model__scale_pos_weight': [1, 3] 
                },
                'LGBMClassifier': {
                    'model__learning_rate': [0.01, 0.1],
                    'model__n_estimators': [100, 200],
                    'model__num_leaves': [31, 50], 
                    'model__boosting_type': ['gbdt', 'dart'],
                    'model__class_weight': [None, 'balanced'] 
                }
            }
            mlflow.set_experiment("Credit_Risk_Model_Training")
            mlflow.sklearn.autolog(log_models=False)
            logging.info('Starting model training and hyperparameter tuning.')
            
            model_report = {}
            best_estimators = {}
            skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
            
            with mlflow.start_run(run_name="Parent_Training_Run"):
                for model_name in models.keys():
                    model = models.get(model_name, 'Model not found')
                    param = params.get(model_name, 'No parameters found')
                    
                    pipeline = Pipeline(steps=[
                        ('smote', SMOTE(random_state=42)),
                        ('model', model)
                    ])
                    gs = GridSearchCV(
                        estimator=pipeline,
                        param_grid=param,
                        scoring='f1',
                        cv=skf,
                        n_jobs=-1,
                        verbose=2
                    )
                    gs.fit(X_train, y_train)
                    model_report[model_name] = gs.best_score_
                    best_estimators[model_name] = gs.best_estimator_
                    
                    logging.info(f"{model_name} best f1 score: {gs.best_score_}")
                    
                best_model_name = max(model_report, key=model_report.get)
                best_model = best_estimators[best_model_name]
            
                mlflow.sklearn.log_model(
                    sk_model=best_model,
                    artifact_path="best_model",
                    registered_model_name="CreditCardDefaultModel"
                )
                mlflow.log_metric("best_f1_score", model_report[best_model_name])
                mlflow.log_param("best_model", best_model_name)
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            logging.info("Model training completed successfully.")
            
            return model_report[best_model_name]
                
        except Exception as e:
            raise CustomException(e, sys)