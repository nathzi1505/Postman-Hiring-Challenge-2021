import configparser
import logging
import time
import sys
import os

import public_api
import public_api_database_handler

config = configparser.ConfigParser()
config.read('config.ini')

time.sleep(5) # Wait for MySQL server to get ready

os.makedirs(f"./logs/", exist_ok=True)
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

sys.stdout = StreamToLogger(log, logging.INFO)
sys.stderr = StreamToLogger(log, logging.ERROR)

DATABASE_URI = config['MYSQL']['URI']

pa   = public_api.PublicApi()
padh = public_api_database_handler.PublicApiDatabaseHandler(DATABASE_URI)

category_list = pa.get_list_of_all_categories()
padh.populate_categories(category_list)

for category in category_list[:1]:
    category_api_list = pa.get_data_for_a_category(category)
    padh.populate_apis_for_category(category, category_api_list)

