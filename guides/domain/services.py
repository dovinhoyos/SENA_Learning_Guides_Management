from guides.models import Guide, PROGRAMAS_FORMACION


def create_guide(title, description, program, file_storage, instructor):
    if program not in PROGRAMAS_FORMACION:
        raise ValueError("Programa inválido.")

    guide = Guide(
        title=title, description=description, program=program, instructor=instructor
    )
    guide.file.put(
        file_storage, content_type="application/pdf", filename=file_storage.filename
    )
    guide.save()
    return guide


def list_all_guides():
    return Guide.objects().select_related()
