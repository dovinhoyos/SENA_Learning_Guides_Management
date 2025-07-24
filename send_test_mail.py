from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"

mail = Mail(app)

with app.app_context():
    msg = Message(
        subject="¡Hola desde Flask!",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=["test@correo.com"],
        body="Este es un test desde Mailtrap y Flask-Mail.",
    )
    mail.send(msg)
    print("✅ Mail enviado (verificalo en Mailtrap)")
