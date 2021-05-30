from pymongo import MongoClient
import os
from dotenv import load_dotenv
from os.path import dirname, join

path_env = join(dirname(__file__), '.env')
load_dotenv(path_env)

LINK_MONGO = os.environ.get('LINK_MONGO')

client = MongoClient(LINK_MONGO)
