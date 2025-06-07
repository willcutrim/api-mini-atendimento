from flask import Flask
from flask_restx import Api
from app.api.routes import ns
from app.api.whatsapp_webhook import whatsapp_bp

def create_app():
    app = Flask(__name__)
    api = Api(app, title="Mini Atendimento IA", version="1.0", description="API com IA e Redis")
    api.add_namespace(ns)
    api.add_namespace(whatsapp_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)

