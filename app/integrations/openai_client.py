import os
import json
import openai
from dotenv import load_dotenv
from app.config.redis_conn import redis_conn

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIClient:
    @staticmethod
    def generate_reply(to, message):
        key = f"context:{to}"
        raw_history = redis_conn.get(key)
        history = json.loads(raw_history) if raw_history else []

        history.append({"role": "user", "content": message})
        full_messages = [{"role": "system", "content": "Você é um atendente virtual simpático."}] + history

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=full_messages
        )

        resposta = response.choices[0].message["content"]
        history.append({"role": "assistant", "content": resposta})
        redis_conn.set(key, json.dumps(history), ex=60 * 5)

        return resposta
