# main.py

import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.exception import CustomException

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
