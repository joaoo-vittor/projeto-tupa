from mongo_connection import client, parse_js, users


class UserModel:

    @classmethod
    def insert_one_user(cls, data):
        if data:
            post_id = users.insert_one(data).inserted_id
            client.close()
            if post_id:
                return post_id
        return None

    @classmethod
    def find_one_user(cls, where={}):
        if where:
            user = users.find_one(where)
            client.close()
            if user:
                return parse_js(user)
        return None

    @classmethod
    def find_by_login(cls, login):
        if login:
            user = users.find_one({'nome_usuario': login})
            client.close()
            if user:
                return parse_js(user)
        return None
