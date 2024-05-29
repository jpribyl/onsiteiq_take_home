from django.contrib.auth import models as auth_models
from django.contrib.auth import models as django_contrib_auth_models
from django.contrib.contenttypes import fields as contenttypes_fields
from django.contrib.contenttypes import models as conttenttypes_models
from django.db import models


class UserObjectPermission(models.Model):
    permission = models.ForeignKey(auth_models.Permission, on_delete=models.CASCADE)
    user = models.ForeignKey(django_contrib_auth_models.User, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/5.0/ref/contrib/contenttypes/
    content_type = models.ForeignKey(
        conttenttypes_models.ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = contenttypes_fields.GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]
