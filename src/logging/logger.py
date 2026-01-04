import logging
import os
from  datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  #gets date time
logs_path = os.path.join(os.getcwd(), "logs")
#the getcwd() function returns the current working directory

os.makedirs(logs_path, exist_ok=True)
#makes new directory if not exists

logging.basicConfig(
    filename=os.path.join(logs_path, LOG_FILE),  #creates log file in logs directory
    format='[%(asctime)s: %(levelname)s: %(name)s]: %(message)s', #log format
    level=logging.INFO, #sets logging level to INFO(there are multiple levels ranging from 0-10-20---50)
)
