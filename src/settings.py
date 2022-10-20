import os
from dotenv import load_dotenv


BOT_NAME = 'beemart_to_prom'
SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'
ROBOTSTXT_OBEY = True

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN", "")
DATA_DIRECTORY = os.getenv("DATA_DIRECTORY", "")
PRODUCTS_FILE = os.getenv("PRODUCTS_FILE", "")
LOGS_FILE = os.getenv("LOGS_FILE", "")
