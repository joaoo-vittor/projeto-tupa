from mongo_connection import client, aluno, users, parse_js
from pymongo import ReturnDocument


class AlunoModel:

    @classmethod
    def insert_aluno(cls, data):
        if data:
            alun = aluno.insert_one(data)
            client.close()
            return True

        return None

    @classmethod
    def find_aluno(cls, id_resp):
        try:
            user = users.find_one({'id_usuario': int(id_resp)})
        except:
            raise FileNotFoundError

        if user:
            return parse_js(user)
        return None

    @classmethod
    def update_aluno(cls, id_resp, new_data):
        try:
            new_user = aluno.find_one_and_update({'id_responsavel': int(id_resp)},
                                                 {'$set': new_data},
                                                 return_document=ReturnDocument.AFTER)
            print(new_user)
        except:
            return None

        if new_user:
            return parse_js(new_user)
        return None
