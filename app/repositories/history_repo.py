import json
from app.config.redis_conn import redis_conn

class HistoryRepo:
    @staticmethod
    def save(to, question, answer, timestamp):
        redis_conn.lpush("message_history", json.dumps({
            "to": to,
            "question": question,
            "answer": answer,
            "timestamp": timestamp
        }))
        redis_conn.ltrim("message_history", 0, 9)

    @staticmethod
    def get_last_messages():
        return [json.loads(msg) for msg in redis_conn.lrange("message_history", -10, -1)]
