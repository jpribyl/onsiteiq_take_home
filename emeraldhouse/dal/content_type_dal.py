from django.contrib.contenttypes.models import ContentType

from emeraldhouse.dataclasses import content_type_dataclasses


def get_by_app_label_and_model(app_label: str, model: str):
    content_type = ContentType.objects.get(app_label=app_label, model=model)
    return content_type_dataclasses.ContentType(
        id=content_type.id,
        app_label=content_type.app_label,
        model=content_type.model,
    )
