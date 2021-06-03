from mongo_connection import client, parse_js, users
from pymongo import ReturnDocument


class UserModel:

    @classmethod
    def insert_one_user(cls, data):
        if data:
            try:
                post_id = users.insert_one(data).inserted_id
                client.close()
            except Exception as e:
                return False

            if post_id:
                return post_id
            return False

        return False

    @classmethod
    def find_user(cls, where={}, filds={'_id': 0, 'senha': 0}):
        if where:
            try:
                user = users.find_one(where, filds)
                client.close()
            except Exception as e:
                return False

            if user:
                return parse_js(user)
            return False

        return False

    @classmethod
    def update_user(cls, where={}, new_data={}):
        if where:
            try:
                user = users.find_one_and_update(where,
                                                 {'$set': new_data},
                                                 projection={
                                                     '_id': 0, 'senha': 0},
                                                 return_document=ReturnDocument.AFTER)

            except Exception as e:
                return False

            if user:
                return parse_js(user)

            return False

        return False
