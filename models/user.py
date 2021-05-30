from mongo_connection import client
from bson import json_util
import json


class UserModel:

    db = client['tupa-database']
    users = db['tupa-users']

    @classmethod
    def insert_one_user(cls, data):
        if data:
            post_id = cls.users.insert_one(data).inserted_id
            if post_id:
                client.close()
                return post_id
        return None

    @staticmethod
    def parse_js(data):
        return json.loads(json_util.dumps(data))

    @classmethod
    def find_one_user(cls, where={}):
        if where:
            user = cls.users.find_one(where)
            if user:
                client.close()
                return cls.parse_js(user)
        return None

    @classmethod
    def find_by_login(cls, login):
        if login:
            user = cls.users.find_one({'nome_usuario': login})
            if user:
                return cls.parse_js(user)
        return None
