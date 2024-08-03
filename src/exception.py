import sys
import logging
from datetime import datetime
import os

# Define the directory for logs
LOG_DIR = os.path.join(os.getcwd(), "logs")

# Create the logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Define the log file name with timestamp
LOGFILE = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Set up logging configuration
logging.basicConfig(
    filename=LOGFILE,  # Log file
    level=logging.INFO,         # Log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S',  # Date format
    filemode='a'  # Append mode
)

def error_message_detail(error, error_detail: sys) -> str:
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, line_number, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
        logging.error(self.error_message)  # Log the error message
    
    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    try:
        logging.info("Program started")
        # Some code that may raise an exception
        a = 1 / 0  # This will raise a ZeroDivisionError
    except Exception as e:
        logging.error("An error occurred")
        raise CustomException(e, sys)
    finally:
        logging.info("Program ended")

    