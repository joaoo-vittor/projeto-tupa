from utils.mongo_connection import client, aluno, parse_js
from pymongo import ReturnDocument


class AlunoModel:

    @classmethod
    def insert_aluno(cls, data):
        if data:
            try:
                alun = aluno.insert_one(data)
                client.close()
            except:
                return False

        if alun:
            return True

        return False

    @classmethod
    def find_aluno(cls, where={}):
        if where:
            try:
                user = aluno.find_one(where, {'_id': 0})
                client.close()
            except:
                return False

        if user:
            return parse_js(user)

        return False

    @classmethod
    def find_alunos(cls, where={}):
        if where:
            try:
                user = aluno.find(where, {'_id': 0})
                client.close()
            except:
                return False

        if user:
            return parse_js(user)

        return False

    @classmethod
    def update_aluno(cls, where={}, new_data={}, filds={'_id': 0}):
        if where and new_data:
            try:
                new_user = aluno.find_one_and_update(where,
                                                     {'$set': new_data},
                                                     projection=filds,
                                                     return_document=ReturnDocument.AFTER)
                client.close()
            except:
                return None

        if new_user:
            return parse_js(new_user)

        return False

    @classmethod
    def delete_aluno(cls, where={}):
        if where:
            try:
                aluno_deleted = aluno.find_one_and_delete(where)
                client.close()
                if aluno_deleted:
                    return True
            except:
                return False

        return False
