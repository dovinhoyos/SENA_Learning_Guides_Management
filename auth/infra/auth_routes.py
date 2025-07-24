from flask import Blueprint, request, jsonify
from auth.domain.auth_service import register_instructor

auth_bp = Blueprint("auth", __name__)


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
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500
