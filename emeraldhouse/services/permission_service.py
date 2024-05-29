from emeraldhouse.dal import content_type_dal, permission_dal
from emeraldhouse.permissions import permission_errors


def verify_user_object_permission(
    user_id: int,
    object_id: int,
    app_label: str,
    model: str,
    permission_codename: str,
):
    content_type = content_type_dal.get_by_app_label_and_model(
        app_label=app_label,
        model=model,
    )

    try:
        permission_dal.get_user_object_permission(
            user_id=user_id,
            object_id=object_id,
            content_type_id=content_type.id,
            permission_codename=permission_codename,
        )
    except permission_errors.MissingObjectPermission:
        return False

    return True


def add_user_object_permission(
    user_id: int,
    object_id: int,
    app_label: str,
    model: str,
    permission_codename: str,
):
    content_type = content_type_dal.get_by_app_label_and_model(
        app_label=app_label,
        model=model,
    )
    permission = permission_dal.get_permission_by_codename(codename=permission_codename)

    return permission_dal.get_or_create_user_object_permission(
        user_id=user_id,
        object_id=object_id,
        content_type_id=content_type.id,
        permission_id=permission.id,
    )
