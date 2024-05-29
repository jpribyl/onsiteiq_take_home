from django.contrib.auth import models as django_contrib_auth_models

from emeraldhouse.dataclasses import permission_dataclasses
from emeraldhouse.models import permission_models
from emeraldhouse.permissions import permission_errors


def get_permission_by_codename(codename: str):
    permission = django_contrib_auth_models.Permission.objects.get(codename=codename)
    return permission_dataclasses.Permission(
        id=permission.id,
        content_type_id=permission.content_type_id,
        codename=permission.codename,
    )


def get_user_object_permission(
    user_id: int, object_id: int, content_type_id: int, permission_codename: str
):
    try:
        user_object_permission = permission_models.UserObjectPermission.objects.get(
            user_id=user_id,
            object_id=object_id,
            content_type_id=content_type_id,
            permission__codename=permission_codename,
        )
    except permission_models.UserObjectPermission.DoesNotExist:
        raise permission_errors.MissingObjectPermission

    return permission_dataclasses.UserObjectPermission(
        user_id=user_object_permission.user_id,
        object_id=user_object_permission.object_id,
        permission_id=user_object_permission.permission_id,
        content_type=user_object_permission.content_type,
    )


def get_or_create_user_object_permission(
    user_id: int,
    object_id: int,
    content_type_id: int,
    permission_id: int,
):
    user_object_permission, _ = (
        permission_models.UserObjectPermission.objects.get_or_create(
            user_id=user_id,
            object_id=object_id,
            content_type_id=content_type_id,
            permission_id=permission_id,
        )
    )

    return permission_dataclasses.UserObjectPermission(
        user_id=user_object_permission.user_id,
        object_id=user_object_permission.object_id,
        permission_id=user_object_permission.permission_id,
        content_type=user_object_permission.content_type,
    )
