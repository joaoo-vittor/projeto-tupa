from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required,  get_jwt_identity
from mongo_connection import parse_js
from datetime import datetime
import math

from models.aluno import AlunoModel

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

        dados.update({'id_responsavel': current_user_id})

        try:
            aluno = AlunoModel.insert_aluno(dados)
        except:
            return {'msg': "could not insert."}, 500

        return parse_js(dados), 201

    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()

        aluno = AlunoModel.find_alunos(
            where={'id_responsavel': current_user_id})

        if aluno:
            return aluno, 200

        return {'msg': 'aluno not found.'}, 404


class AlunoParams(Resource):

    @jwt_required()
    def put(self, id_aluno):
        dados = params.parse_args()
        current_user_id = get_jwt_identity()

        dados = {k: dados[k] for k in dados.keys() if dados[k] != None}
        dados.pop('id_responsavel')
        dados.pop('id_crianca')

        new_al = AlunoModel.update_aluno(where={
            'id_crianca': id_aluno,
            'id_responsavel': current_user_id},
            new_data=dados)

        if new_al:
            return new_al, 200
        return {'msg': 'could not update.'}, 500

    @jwt_required()
    def get(self, id_aluno):
        current_user_id = get_jwt_identity()

        aluno = AlunoModel.find_aluno(where={
            'id_crianca': id_aluno,
            'id_responsavel': current_user_id})

        if aluno:
            return aluno, 200

        return {'msg': 'aluno not found.'}, 404

    @jwt_required()
    def delete(self, id_aluno):
        current_user_id = get_jwt_identity()
        del_aluno = AlunoModel.delete_aluno(where={
            'id_crianca': id_aluno,
            'id_responsavel': current_user_id})

        if del_aluno:
            return {'msg': 'successfully deleted.'}, 200

        return {'msg': 'it was not possible to delete.'}, 400
