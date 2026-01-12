import logging
import os
from  datetime import datetime


def setup_logging():
    """Sets up logging configuration for the application.
    """

    #the getcwd() function returns the current working directory
    log_dir = os.path.join(os.getcwd(), "logs")
    #makes new directory if not exists
    os.makedirs(log_dir, exist_ok=True)

    #gets date time
    log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    log_path = os.path.join(log_dir, log_file)


    logging.basicConfig(
         #sets logging level to INFO(there are multiple levels ranging from 0-10-20---50)
        level=logging.INFO,
        format='[%(asctime)s: %(levelname)s: %(name)s]: %(message)s', #log format
        handlers=[
            logging.FileHandler(log_path), #file handler to write logs to file
            logging.StreamHandler()  #stream handler to output logs to console
        ]
    )
