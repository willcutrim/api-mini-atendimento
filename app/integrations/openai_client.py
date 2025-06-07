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
        full_messages = [
            {
                "role": 
                "system", 
                "content": (
                    "Você é um atendente virtual da empresa FaturaFácil. "
                    "Seu papel é ajudar o cliente com dúvidas sobre seus débitos fictícios. "
                    "Sempre que o cliente perguntar sobre débitos, gere uma lista com até 3 cobranças fictícias, "
                    "incluindo o nome do serviço, valor e data de vencimento. "
                    "Você deve parecer um atendente humano, usando linguagem cordial e clara. "
                    "Exemplo de resposta: "
                    "\"Verifiquei aqui e encontrei 2 débitos em aberto:\n"
                    "1. Plano Premium - R$ 89,90 - Vencimento: 10/05/2025\n"
                    "2. Mensalidade Academia - R$ 59,00 - Vencimento: 05/06/2025\n"
                    "Caso precise de ajuda para regularizar, posso te orientar.\""
                )
            }
        ] + history

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=full_messages
        )

        resposta = response.choices[0].message["content"]
        history.append({"role": "assistant", "content": resposta})
        redis_conn.set(key, json.dumps(history), ex=60 * 5)

        return resposta
