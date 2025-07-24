import io

from flask import Blueprint, jsonify, request, send_file
from flask_login import current_user, login_required

from guides.domain.services import create_guide, list_all_guides
from guides.models import Guide

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
    except Exception:
        return jsonify({"error": "Error al subir la guía"}), 500


@guides_bp.route("/guides", methods=["GET"])
@login_required
def list_guides():
    guides = list_all_guides()

    result = []
    for guide in guides:
        result.append(
            {
                "id": str(guide.id),
                "title": guide.title,
                "description": guide.description,
                "program": guide.program,
                "instructor": guide.instructor.full_name,
                "regional": guide.instructor.regional,
                "created_at": guide.created_at.isoformat(),
                "pdf_url": f"/guides/{str(guide.id)}/pdf",
            }
        )

    return jsonify(result), 200


@guides_bp.route("/guides/<guide_id>/pdf", methods=["GET"])
@login_required
def download_pdf(guide_id):
    guide = Guide.objects(id=guide_id).first()
    if not guide or not guide.file:
        return jsonify({"error": "Guía no encontrada"}), 404

    return send_file(
        io.BytesIO(guide.file.read()),
        mimetype="application/pdf",
        download_name=guide.file.filename,
        as_attachment=False,  # Cambialo a True si querés que se descargue
    )
