from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,  get_jwt_identity
from mongo_connection import parse_js
from datetime import datetime
import math

from models.aluno import AlunoModel

params = reqparse.RequestParser()
params = reqparse.RequestParser()

params.add_argument('nome', type=str, required=False)
params.add_argument('id_crianca', type=int,
                    default=math.ceil(datetime.timestamp(datetime.now())))

params.add_argument('data_nascimento', type=str, required=False)
params.add_argument('idade', type=int)
params.add_argument('sexo', type=str, required=False)
params.add_argument('nome_responsavel', type=str, required=False)
params.add_argument('id_responsavel', type=int,
                    default=math.ceil(datetime.timestamp(datetime.now())))

params.add_argument('escola', type=str, required=False)
params.add_argument('cep', type=int)
params.add_argument('endareco', type=str, required=False)
params.add_argument('bairro', type=str, required=False)
params.add_argument('unidade_de_saude', type=str, required=False)
params.add_argument('data_de_acompanhamento', type=str, required=False)
params.add_argument('peso_kg', type=int)
params.add_argument('altura_cm', type=int)
params.add_argument('imc', type=int)
params.add_argument('imc_normalizado', type=int)
params.add_argument('classificacao_estatura', type=str, required=False)
params.add_argument('classificacao_imc', type=str, required=False)
params.add_argument('classificacao_imc_mr', type=str, required=False)
params.add_argument('score_consumo_alimentar', type=int)
params.add_argument('classificacao_consumo_alimentar',
                    type=str, required=False)
params.add_argument('score_escola', type=int)
params.add_argument('classificacao_escola', type=int)


class Aluno(Resource):

    @jwt_required()
    def post(self):
        dados = params.parse_args()
        current_user_id = get_jwt_identity()

        responsavel = AlunoModel.find_aluno(current_user_id)
        dados.update({'id_responsavel': current_user_id})

        if responsavel:
            AlunoModel.insert_aluno(dados)
            return parse_js(dados), 201

        return {'msg': "'responsavel' not found."}, 404

    @jwt_required()
    def put(self):
        dados = params.parse_args()
        current_user_id = get_jwt_identity()

        dados = {k: dados[k] for k in dados.keys() if dados[k] != None}
        dados.pop('id_responsavel')
        dados.pop('id_crianca')

        new_al = AlunoModel.update_aluno(current_user_id, dados)

        if new_al:
            return new_al, 200
        return {'msg': "could not update."}, 500
