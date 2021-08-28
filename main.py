# -------------------------------------------------------------------------
# Name:         PublicApis Main Crawler (Postman Hiring Challenge - 2021)
# Created By:   Pritthijit Nath
# Email:        pritthijit.nath@icloud.com
# Place:        Kolkata, India
# -------------------------------------------------------------------------

import configparser
import logging
import time
import sys
import os

import public_api
import public_api_database_handler

# Reading the config.ini file to extract the DATABASE connection string
config = configparser.ConfigParser()
config.read('config.ini')

time.sleep(10)  # Waiting for MySQL server to get ready

# Organising the file structure to place the logs
os.makedirs(f"./logs/", exist_ok=True)

# Initializing the logging object + ensuring the timezone being used is UTC
logging.basicConfig(filename=f"logs/apicrawler_{int(time.time())}.log",
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a+')
logging.Formatter.converter = time.gmtime


class StreamToLogger(object):
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Redirecting the stdout and stderr to logs
sys.stdout = StreamToLogger(log, logging.INFO)
sys.stderr = StreamToLogger(log, logging.ERROR)

# Extracting the MySQL Database Connection String
DATABASE_URI = config['MYSQL']['URI']

# Initializing the required class instances
pa = public_api.PublicApi()
padh = public_api_database_handler.PublicApiDatabaseHandler(DATABASE_URI)

# Extracting the category list 
# + Saving the categories into the database
category_list = pa.get_list_of_all_categories()
padh.populate_categories(category_list)

# Extracting the api data for each category 
# + Saving the data into the database (category by category)
for category in category_list:
    category_api_list = pa.get_data_for_a_category(category)
    padh.populate_apis_for_category(category, category_api_list)

print("Fetch completed.")
