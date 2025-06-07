import datetime
import json

from app.config.redis_conn import redis_conn
from app.integrations.openai_client import OpenAIClient
from app.repositories.history_repo import HistoryRepo

class MessageService:
    @staticmethod
    def enqueue_message(to, message):
        redis_conn.lpush("message_queue", json.dumps({"to": to, "message": message}))

    @staticmethod
    def get_last_messages():
        return HistoryRepo.get_last_messages()
    
    @staticmethod
    def process_message(to, message):
        resposta = OpenAIClient.generate_reply(to, message)
        HistoryRepo.save(to, message, resposta, datetime.utcnow().isoformat())
        return resposta
