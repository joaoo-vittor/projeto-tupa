import os
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os.path import dirname, join
from datetime import datetime
import math

from models.user import UserModel
from blocklist import BLOCKLIST

params = reqparse.RequestParser()

params.add_argument('id_usuario', type=int,
                    default=math.ceil(datetime.timestamp(datetime.now())))
params.add_argument('nome', type=str)
params.add_argument('nome_usuario', type=str, required=True,
                    help="O campo 'nome_usuario' não pode ficar vazio.")
params.add_argument('senha', type=str, required=True,
                    help="O campo 'senha' não pode ficar vazio.")
params.add_argument('tipo', type=str, default='responsavel')


path_env = join(dirname(__file__), '.env')
load_dotenv(path_env)


class User(Resource):

    def get(self, name):
        user = UserModel.find_by_login(name)

        if user:
            return user, 200
        return {'msg': f'User "{name}" not found.'}, 404


class UserRegister(Resource):

    def post(self):
        dados = params.parse_args()

        senha = generate_password_hash(dados['senha'])
        dados.update({'senha': senha.replace(os.environ.get('HASH'), '')})

        if UserModel.find_by_login(dados['nome_usuario']):
            return {'msg': f'User already exists.'}, 400

        try:
            user = UserModel.insert_one_user(dados)
        except:
            return {'msg': 'Inserted error.'}, 500

        return {'msg': 'User {} was inserted with success.'.format(dados['nome'])}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = params.parse_args()
        user = UserModel.find_by_login(
            dados['nome_usuario'], filter={'_id': 0})

        if user:
            if check_password_hash(os.environ.get('HASH')+user['senha'],
                                   dados['senha']):

                access_token = create_access_token(
                    identity=user['id_usuario'])
                return {'access_token': access_token}, 200

            return {'msg': 'Password incorrect.'}, 401

        return {'msg': 'User not found.'}, 404


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']  # JWT Token Indentifier
        BLOCKLIST.add(jwt_id)
        return {'msg': 'Desconectado com sucesso!'}, 200
