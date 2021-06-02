from mongo_connection import client, aluno, parse_js
from pymongo import ReturnDocument


class AlunoModel:

    @classmethod
    def insert_aluno(cls, data):
        if data:
            try:
                alun = aluno.insert_one(data)
            except:
                return False

            client.close()
            return True

        return None

    @classmethod
    def find_aluno(cls, filter={}):
        try:
            if filter:
                user = aluno.find_one(filter, {'_id': 0})
                client.close()
        except:
            return False

        if user:
            return parse_js(user)
        return None

    @classmethod
    def find_alunos(cls, filter={}):
        try:
            if filter:
                user = aluno.find(filter, {'_id': 0})
                client.close()
        except:
            return False

        if user:
            return parse_js(user)
        return None

    @classmethod
    def update_aluno(cls, filter={}, new_data={}):
        try:
            if filter and new_data:
                new_user = aluno.find_one_and_update(filter,
                                                     {'$set': new_data},
                                                     return_document=ReturnDocument.AFTER)
                client.close()
        except:
            return None

        if new_user:
            return parse_js(new_user)
        return None

    @classmethod
    def delete_aluno(cls, filter={}):
        try:
            aluno_deleted = aluno.find_one_and_delete(filter)
            if aluno_deleted:
                return True
        except:
            return False
