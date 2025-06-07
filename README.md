
# Mini Atendimento com IA

## Como rodar

1. Configure o `.env` com sua chave da OpenAI:
OPENAI_API_KEY=sk-...
REDIS_HOST=redis

2. Suba com Docker:
docker compose up --build

3. Acesse:
- Swagger: http://localhost:5000/apidocs
- POST /send-message
- GET /history
