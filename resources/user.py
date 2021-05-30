from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import UserModel

params = reqparse.RequestParser()
params.add_argument('nome')
params.add_argument('nome_usuario')
params.add_argument('senha')
params.add_argument('tipo')


class User(Resource):
    def get(self, name):
        user = UserModel.find_one_user({'nome': name})
        if user:
            return user, 200
        return {'msg': f'User "{name}" not found.'}, 404


class UserRegister(Resource):

    def post(self):
        dados = params.parse_args()

        senha = generate_password_hash(dados['senha'])
        dados.update({'senha': senha})

        if UserModel.find_one_user({'nome': dados['nome']}):
            return {'msg': f'User already exists.'}, 400

        try:
            user = UserModel.insert_one_user(dados)
        except:
            return {'msg': 'Inserted error.'}, 500

        return {'msg': 'User {} was inserted with success.'.format(dados['nome'])}


class UserLogin(Resource):

    def post(cls):
        dados = params.parse_args()
        user = UserModel.find_by_login(dados['nome_usuario'])

        if user:
            if check_password_hash(user['senha'], dados['senha']):
                access_token = create_access_token(
                    identity=user['nome_usuario'])
                return {'access_token': access_token}, 200

            return {'msg': 'Password incorrect.'}, 401

        return {'msg': 'User not found.'}, 404
