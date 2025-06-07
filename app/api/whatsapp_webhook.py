import requests
import os

from flask import Blueprint, request, jsonify

from app.services.message_service import MessageService

whatsapp_bp = Blueprint('whatsapp_webhook', __name__)

@whatsapp_bp.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == os.getenv("WHATSAPP_VERIFY_TOKEN"):
        return challenge, 200
    return "Forbidden", 403

@whatsapp_bp.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages")
                if messages:
                    message = messages[0]
                    phone = message["from"]
                    text = message["text"]["body"]

                    resposta = MessageService.process_message(phone, text)

                    payload = {
                        "messaging_product": "whatsapp",
                        "to": phone,
                        "type": "text",
                        "text": {"body": resposta}
                    }
                    headers = {
                        "Authorization": f"Bearer {os.getenv("WHATSAPP_TOKEN")}",
                        "Content-Type": "application/json"
                    }
                    requests.post(f"{os.getenv("WHATSAPP_API_URL")}/messages", json=payload, headers=headers)

    except Exception as e:
        print("Erro ao processar mensagem do WhatsApp:", str(e))
    return jsonify({"status": "received"}), 200