from app.config.redis_conn import redis_conn
from app.integrations.openai_client import OpenAIClient
from app.repositories.history_repo import HistoryRepo
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

def run_worker():
    print("👂 Worker iniciado. Escutando mensagens na fila...")
    while True:
        payload = redis_conn.blpop("message_queue")
        if payload:
            data = json.loads(payload[1])
            to = data["to"]
            message = data["message"]

            print(f"📨 Mensagem recebida de {to}: {message}")
            resposta = OpenAIClient.generate_reply(to, message)
            print(f"🤖 Resposta gerada: {resposta}")

            HistoryRepo.save(to, message, resposta, datetime.utcnow().isoformat())

if __name__ == "__main__":
    run_worker()
