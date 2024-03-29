import datetime
import logging
import os

# Get the directory name of the file
file_path = "./logs/"

# Create the directory if it does not exist
if not os.path.exists(file_path):
    os.makedirs(file_path)


# This option will
# create a log file for each run
# curr_time = datetime.datetime.now()
# log_file_name = file_path + curr_time.strftime("logs_%Y-%m-%d_%H-%M-%S.log")
# with open(log_file_name, "w"):
#     pass


# overwriting one logging file before a run
# log_file_name = file_path + "logs.log"
# with open(log_file_name, "w"):
#     pass

# DVC will overwrite the log file for every running stage
# Therefore we do not let it overwrite
log_file_name = file_path + "logs.log"


# variable checker logger
a03_logger = logging.getLogger("A03 Logger")
a03_logger.setLevel(logging.DEBUG)
a03_handler = logging.FileHandler(log_file_name)
a03_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
a03_handler.setFormatter(a03_formatter)
a03_logger.addHandler(a03_handler)

