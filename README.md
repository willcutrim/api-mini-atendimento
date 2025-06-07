# Mini Atendimento IA

Este projeto é uma aplicação Flask com integração a uma IA via OpenAI, Redis para enfileiramento, e suporte opcional ao WhatsApp usando a API oficial da Meta.

---

## ✅ Requisitos

- Python 3.11 (algumas bibliotecas requerem esta versão para funcionar corretamente)
- Docker (opcional, mas recomendado)
- Redis
- Conta e token da API oficial do WhatsApp (opcional)

---

## 🐍 Rodando localmente (sem Docker)

1. Instale o Python 3.11 (recomendado usar pyenv):
```bash
pyenv install 3.11.9
pyenv local 3.11.9
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo `.env` com o seguinte conteúdo:

```env
REDIS_HOST=redis
OPENAI_API_KEY=sk-...

# Só preencha esses se for usar a integração com o WhatsApp oficial
WHATSAPP_TOKEN=seu_token
WHATSAPP_API_URL=https://graph.facebook.com/v18.0/NUMERO/messages
WHATSAPP_VERIFY_TOKEN=seu_token_de_verificacao
```

> ❗ Se **não for usar o WhatsApp**, comente a linha:
> - `api.add_namespace(whatsapp_bp)` em `run.py`
> - `api.add_namespace(whatsapp_bp, path="/whatsapp-hook")` em `main.py`

---

## 🐳 Rodando com Docker

```bash
sudo docker compose up --build
```

O sistema sobe:
- Flask API em `http://localhost:5000`
- Redis no container `redis`
- Worker para processar mensagens

---

## 📚 Rotas disponíveis

| Método | Rota                        | Descrição |
|--------|-----------------------------|-----------|
| POST   | `/mensagens/send-message`   | Enfileira mensagem para a IA |
| GET    | `/mensagens/history`        | Exibe os últimos 10 atendimentos |
| DELETE | `/mensagens/reset-context/<to>` | Reseta o contexto de um número |
| POST   | `/whatsapp-hook` (opcional) | Webhook para receber mensagens do WhatsApp oficial |

---

## 🤖 Sobre a IA

Este projeto utiliza a **API da OpenAI** (via `openai.ChatCompletion`) para gerar respostas automáticas com contexto por número de telefone.

---

## ✝️
**Deus seja louvado.**