from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from auth.domain.auth_service import register_instructor
from auth.models import Instructor

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    instructor = Instructor.objects(email=email).first()
    if not instructor:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not check_password_hash(instructor.password, password):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    login_user(instructor)
    return jsonify({"message": "Login exitoso", "instructor_id": str(instructor.id)})


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    try:
        instructor = register_instructor(
            full_name=data["full_name"],
            email=data["email"],
            regional_str=data["regional"],
        )
        return jsonify(
            {
                "message": "Instructor registrado correctamente.",
                "instructor_id": str(instructor.id),
            }
        ), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@auth_bp.route("/auth/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Sesión cerrada"})


@auth_bp.route("/auth/me")
@login_required
def me():
    return jsonify({"message": f"Sesión activa de: {current_user.full_name}"})
