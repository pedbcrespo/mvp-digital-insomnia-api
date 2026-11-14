from urllib import response

from flask import request
from flask_restx import Namespace, Resource, fields
from service import SleepPredictionService

sleep_prediction_ns = Namespace('sleep-prediction', description='Operações relacionadas a previsão de sono')

service = SleepPredictionService()


sleep_prediction_request_model = sleep_prediction_ns.model('SleepPredictionRequest', {
    'age': fields.Integer(required=True, description='Idade do usuário'),
    'gender': fields.String(required=True, description='Gênero do usuário'),
    'chronotype': fields.String(required=True, description='Cronotipo do usuário'),
    'occupation': fields.String(required=True, description='Ocupação do usuário'),
    'bedtime_hour': fields.Float(required=True, description='Hora de dormir do usuário'),
    'screen_time_before_bed_min': fields.Integer(required=True, description='Tempo de tela antes de dormir em minutos'),
    'primary_app_category': fields.String(required=True, description='Categoria principal do aplicativo usado antes de dormir'),
    'screen_brightness_pct': fields.Integer(required=True, description='Brilho da tela em porcentagem'),
    'blue_light_filter_on': fields.Boolean(required=True, description='Se o filtro de luz azul está ativado'),
    'caffeine_intake_mg': fields.Integer(required=True, description='Ingestão de cafeína em miligramas'),
    'caffeine_last_hour': fields.Float(required=True, description='Última hora de ingest    ão de cafeína'),
    'physical_activity_min': fields.Integer(required=True, description='Atividade física em minutos'),
    'room_temperature_f': fields.Float(required=True, description='Temperatura do quarto em Fahrenheit'),
    'ambient_noise_db': fields.Float(required=True, description='Nível de ruído ambiente em decibéis'),
})

sleep_prediction_response_model = sleep_prediction_ns.model('SleepPredictionResponse', {
    'prediction': fields.String(required=True, description='A previsão de sono')
})

error_model = sleep_prediction_ns.model('Error', {
    'error': fields.String,
})

@sleep_prediction_ns.route('/predict')
class SleepPrediction(Resource):
    @sleep_prediction_ns.expect(sleep_prediction_request_model, validate=True)
    @sleep_prediction_ns.marshal_with(sleep_prediction_response_model, code=200)
    @sleep_prediction_ns.response(400, 'Erro ao registrar previsão de sono', error_model)
    def post(self):
        pass