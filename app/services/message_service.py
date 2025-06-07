import json
from app.config.redis_conn import redis_conn
from app.repositories.history_repo import HistoryRepo

class MessageService:
    @staticmethod
    def enqueue_message(to, message):
        redis_conn.lpush("message_queue", json.dumps({"to": to, "message": message}))

    @staticmethod
    def get_last_messages():
        return HistoryRepo.get_last_messages()
