from django.conf import settings
from pymongo.mongo_client import MongoClient
from django.utils import timezone
from src.data_module import get_ltp

client = MongoClient(settings.RAN_ON, 27017)
database=client['PROJECT']

strategy=database['STRATEGY']
strategy_positions=database['STRATEGY_POSITIONS']
strategy_orders=database['STRATEGY_ORDERS']

users=database['USERS']
users_positions=database['USERS_POSITIONS']
users_orders=database['USERS_ORDERS']

import logging
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')

