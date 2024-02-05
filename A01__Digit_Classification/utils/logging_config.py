import logging
import os
import datetime

# Get the directory name of the file
file_path = "./logs/"

# Create the directory if it does not exist
if not os.path.exists(file_path):
    os.makedirs(file_path)


# create a log file for each run
curr_time = datetime.datetime.now()
log_file_name = file_path + curr_time.strftime("logs_%Y-%m-%d_%H-%M-%S.log")
# with open(log_file_name, "w"):
#     pass


# overwriting one logging file before a run
log_file_name = file_path + "logs.log"
with open(log_file_name, "w"):
    pass


# variable checker logger
var_chk_logger = logging.getLogger("VARIBLE CHECKS")
var_chk_logger.setLevel(logging.DEBUG)
var_chk_handler = logging.FileHandler(log_file_name)
var_chk_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
var_chk_handler.setFormatter(var_chk_formatter)
var_chk_logger.addHandler(var_chk_handler)


# script running logger
script_run_logger = logging.getLogger("SCRIPT RUNNER")
script_run_logger.setLevel(logging.INFO)
script_run_handler = logging.FileHandler(log_file_name)
script_run_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
script_run_handler.setFormatter(script_run_formatter)
script_run_logger.addHandler(script_run_handler)
