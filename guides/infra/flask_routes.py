from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from guides.domain.services import create_guide

guides_bp = Blueprint("guides", __name__)


@guides_bp.route("/guides/upload", methods=["POST"])
@login_required
def upload_guide():
    title = request.form.get("title")
    description = request.form.get("description")
    program = request.form.get("program")
    file = request.files.get("file")

    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Se requiere un archivo PDF"}), 400

    try:
        guide = create_guide(title, description, program, file, current_user)
        return jsonify(
            {"message": "Guía subida correctamente", "guide_id": str(guide.id)}
        ), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Error al subir la guía"}), 500
