import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from mongoengine import connect

mail = Mail()
login_manager = LoginManager()


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Flask-Mail config
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"

    mail.init_app(app)
    login_manager.init_app(app)

    # Conexión a MongoDB
    connect(host=os.getenv("MONGO_URI"))

    return app
