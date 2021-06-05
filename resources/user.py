import os
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token,
                                jwt_required,
                                get_jwt,
                                get_jwt_identity)

from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os.path import dirname, join
from datetime import datetime
import math

from models.user import UserModel
from utils.blocklist import BLOCKLIST

params = reqparse.RequestParser()

params.add_argument('id_usuario', type=int,
                    default=math.ceil(datetime.timestamp(datetime.now())))
params.add_argument('nome', type=str)
params.add_argument('nome_usuario', type=str, required=True,
                    help="O campo 'nome_usuario' não pode ficar vazio.")
params.add_argument('senha', type=str, required=True,
                    help="O campo 'senha' não pode ficar vazio.")
params.add_argument('tipo', type=str, default='responsavel')

alter_params = reqparse.RequestParser()
alter_params.add_argument('nome', type=str)
alter_params.add_argument('nome_usuario', type=str)
alter_params.add_argument('senha', type=str)
alter_params.add_argument('nova_senha', type=str)
alter_params.add_argument('tipo', type=str)


path_env = join(dirname(__file__), '.env')
load_dotenv(path_env)


class User(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_user(where={'id_usuario': int(user_id)})

        if user:
            return user, 200
        return {'msg': 'User not found.'}, 404

    @jwt_required()
    def put(self):
        dados = alter_params.parse_args()
        dados = {k: dados[k] for k in dados.keys() if dados[k] is not None}

        user_id = get_jwt_identity()

        if 'nome_usuario' in dados.keys():

            user = UserModel.find_user(
                where={'nome_usuario': dados['nome_usuario']})

            if user and user['id_usuario'] != user_id:
                return {'msg': 'User already exists.'}, 400

        if 'senha' in dados.keys() and 'nova_senha' in dados.keys():
            user = UserModel.find_user(where={'id_usuario': user_id},
                                       filds={'_id': 0})

            if check_password_hash(os.environ.get('HASH')+user['senha'],
                                   dados['senha']):

                new_senha = generate_password_hash(dados['nova_senha'])

                new_senha = new_senha.replace(os.environ.get('HASH'), '')

                dados.update({'senha':
                              new_senha.replace(os.environ.get('HASH'), '')})

                updated_user = UserModel.update_user(where={'id_usuario': user_id},
                                                     new_data={'senha': new_senha})

                if updated_user:
                    return updated_user, 200

                return {'msg': 'error updating.'}, 500

            return {'msg': 'invalid password.'}, 400

        else:
            updated_user = UserModel.update_user(where={'id_usuario': user_id},
                                                 new_data=dados)

            if updated_user:
                return updated_user, 200

            return {'msg': 'error updating.'}, 500


class UserRegister(Resource):

    def post(self):
        dados = params.parse_args()

        senha = generate_password_hash(dados['senha'])
        dados.update({'senha': senha.replace(os.environ.get('HASH'), '')})

        if UserModel.find_user({'nome_usuario': dados['nome_usuario']}):
            return {'msg': 'User already exists.'}, 400

        try:
            user = UserModel.insert_one_user(dados)
        except:
            return {'msg': 'Inserted error.'}, 500

        if user:
            return {'msg': 'User {} was inserted with success.'.format(dados['nome'])}

        return {'msg': 'Inserted error.'}, 500


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = params.parse_args()
        user = UserModel.find_user(
            where={'nome_usuario': dados['nome_usuario']}, filds={'_id': 0})

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
        return {'msg': 'Successfully disconnected!'}, 200
