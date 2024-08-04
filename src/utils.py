import os
import sys
import dill
from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        # Extract the directory path from the file path
        dir_path = os.path.dirname(file_path)
        
        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)
        
        # Open the file in binary write mode and save the object using dill
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    
    except Exception as e:
        # Raise a CustomException if an error occurs
        raise CustomException(e, sys)
