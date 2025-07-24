import secrets
from auth.models import Instructor, RegionalEnum
from shared.config import mail
from flask_mail import Message
from werkzeug.security import generate_password_hash


def generate_password():
    return secrets.token_urlsafe(8)


def send_registration_email(email, password):
    msg = Message(
        subject="Registro en SENA Learning App",
        sender="noreply@senaapp.com",
        recipients=[email],
        body=f"Bienvenido/a!\n\nTus credenciales son:\nUsuario: {email}\nContraseña: {password}",
    )
    mail.send(msg)


def register_instructor(full_name, email, regional_str):
    if regional_str not in [r.value for r in RegionalEnum]:
        raise ValueError("Regional no válido.")

    existing = Instructor.objects(email=email).first()
    if existing:
        raise ValueError("Ya existe un instructor con ese correo.")

    password = generate_password()
    password_hashed = generate_password_hash(password)

    instructor = Instructor(
        full_name=full_name,
        email=email,
        regional=regional_str,
        password=password_hashed,
    )
    instructor.save()

    send_registration_email(email, password)
    return instructor
