from flask import Flask
from flask_restx import Api
from app.api.routes import ns  # importa o namespace

def create_app():
    app = Flask(__name__)
    api = Api(app, title="Mini Atendimento IA", version="1.0", description="API com IA e Redis")
    api.add_namespace(ns, path="/mensagens")
    return app
