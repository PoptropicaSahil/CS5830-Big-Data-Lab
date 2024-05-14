import datetime
import logging
import os

# Get the directory name of the file
file_path = "./logs/"

# Create the directory if it does not exist
if not os.path.exists(file_path):
    os.makedirs(file_path)


# overwriting one logging file before a run
log_file_name = file_path + "logs.log"

with open(log_file_name, "w"):
    pass


# script running logger
script_run_logger = logging.getLogger("SCRIPT RUNNER")
script_run_logger.setLevel(logging.INFO)
script_run_handler = logging.FileHandler(log_file_name)
script_run_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
script_run_handler.setFormatter(script_run_formatter)
script_run_logger.addHandler(script_run_handler)
