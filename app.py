import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from dotenv import load_dotenv
from os.path import dirname, join


from resources.user import User, UserRegister, UserLogin, UserLogout
from resources.aluno import Aluno, AlunoParams, AlunoSaveFile, AlunoGetFile
from utils.blocklist import BLOCKLIST


# Variaveis de Ambiente
path_env = join(dirname(__file__), '.env')
load_dotenv(path_env)

app = Flask(__name__)

# Configurações do Flask
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=20)

api = Api(app)
jwt = JWTManager(app)


# Verificação se o token está na BLOCKLIST
@jwt.token_in_blocklist_loader
def verifica_token(self, token):
    return token['jti'] in BLOCKLIST


# Verificação se o token foi revogado
@jwt.revoked_token_loader
def token_de_acesso_invalido(jwt_header, jwt_payload):
    return jsonify({'msg': 'você está deslogado.'}), 401


# Rotas
api.add_resource(User, '/user')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Aluno, '/aluno')
api.add_resource(AlunoParams, '/aluno/<int:id_aluno>')
api.add_resource(AlunoSaveFile, '/aluno/file')
api.add_resource(AlunoGetFile, '/aluno/file/<string:name_file>')


if __name__ == '__main__':
    app.run(debug=True)

# def create_app():
#     return app
