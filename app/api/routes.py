from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.message_service import MessageService
from app.config.redis_conn import redis_conn

ns = Namespace('mensagens', description='Operações de mensagem')

mensagem_model = ns.model('Mensagem', {
    'to': fields.String(required=True, example='+5511999999999'),
    'message': fields.String(required=True, example='Quero saber sobre meus débitos')
})

historico_model = ns.model('Historico', {
    'to': fields.String(),
    'question': fields.String(),
    'answer': fields.String(),
    'timestamp': fields.String()
})

@ns.route('/send-message')
class SendMessage(Resource):
    @ns.expect(mensagem_model)
    @ns.response(202, 'Mensagem enfileirada com sucesso')
    def post(self):
        data = request.get_json()
        MessageService.enqueue_message(data["to"], data["message"])
        return {"status": "enqueued"}, 202

@ns.route('/history')
class History(Resource):
    @ns.marshal_list_with(historico_model)
    def get(self):
        return MessageService.get_last_messages(), 200

@ns.route('/reset-context/<string:to>')
class ResetContext(Resource):
    def delete(self, to):
        key = f"context:{to}"
        redis_conn.delete(key)
        return '', 204
