import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from src.components.data_ingestion import DataIngestion
from src.components.data_ingestion import DataIngestionConfig

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifact', "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self) -> ColumnTransformer:
        '''
        This function is responsible for the Data Transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                'gender', 'race_ethnicity', 
                'parental_level_of_education', 'lunch', 
                'test_preparation_course'
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scalar", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scalar", StandardScaler(with_mean=False))  # Set with_mean=False for compatibility with sparse output
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path: str, test_path: str):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and test dataframe"
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, 
                np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, 
                np.array(target_feature_test_df)
            ]

            logging.info(f"Saving preprocessing object.")
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj= preprocessing_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        logging.info("Starting data ingestion process.")
        ingestion = DataIngestion()
        train_data, test_data = ingestion.initiate_data_ingestion()

        logging.info("Starting data transformation process.")
        transformation = DataTransformation()
        train_arr, test_arr, preprocessor_path = transformation.initiate_data_transformation(train_data, test_data)

        logging.info("Data transformation process completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during data transformation: {str(e)}")
