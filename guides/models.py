from datetime import datetime, timezone

from mongoengine import DateTimeField, Document, FileField, ReferenceField, StringField

from auth.models import Instructor

PROGRAMAS_FORMACION = [
    "Desarrollo de Software",
    "Multimedia",
    "Inteligencia Artificial",
    "Analítica de Datos",
    "Construcción",
    "Contabilidad",
]


class Guide(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    program = StringField(required=True, choices=PROGRAMAS_FORMACION)
    instructor = ReferenceField(Instructor, required=True)
    file = FileField(required=True)  # Usamos GridFS para PDFs
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
