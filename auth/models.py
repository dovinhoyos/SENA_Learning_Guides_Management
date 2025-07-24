import enum
from mongoengine import Document, StringField, EmailField
from flask_login import UserMixin


class RegionalEnum(enum.Enum):
    CAUCA = "Cauca"
    HUILA = "Huila"
    ANTIOQUIA = "Antioquia"
    VALLE = "Valle"
    NARIÑO = "Nariño"


class Instructor(Document, UserMixin):
    full_name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    regional = StringField(required=True, choices=[r.value for r in RegionalEnum])
    password = StringField(required=True)  # Hasheada en una futura mejora

    def get_id(self):
        return str(self.id)
