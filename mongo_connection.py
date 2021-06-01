from pymongo import MongoClient
import os
from dotenv import load_dotenv
from os.path import dirname, join
from bson import json_util
import json


path_env = join(dirname(__file__), '.env')
load_dotenv(path_env)

client = MongoClient(os.environ.get('LINK_MONGO'))

# Base
db = client['tupa-database']

# collections
users = db['tupa-users']
aluno = db['tupa-aluno']


def parse_js(data):
    return json.loads(json_util.dumps(data))
