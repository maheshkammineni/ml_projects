import logging
import sys
from datetime import datetime
import os
# Get the current working directory
cwd = os.getcwd()

# Define the directory for logs
LOG_DIR = os.path.join(cwd, "logs")

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

