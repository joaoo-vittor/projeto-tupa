import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
from dotenv import load_dotenv
from os.path import dirname, join

from resources.user import User, UserRegister, UserLogin

path_env = join(dirname(__file__), '.env')
load_dotenv(path_env)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)

api = Api(app)
jwt = JWTManager(app)

api.add_resource(User, '/user/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    app.run(debug=True)
