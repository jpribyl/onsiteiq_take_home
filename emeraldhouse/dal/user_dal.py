from django.contrib.auth.models import Group, User

from emeraldhouse.dataclasses import user_dataclasses


def get_or_create(
    first_name: str,
    last_name: str,
    email: str,
) -> user_dataclasses.User:
    user, _ = User.objects.get_or_create(
        # This is a result of the django contrib auth user model. It
        # enforces uniqueness on the username rather than the email.
        username=email,  # TODO: replace user with custom user and enforce email uniqueness
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    return user_dataclasses.User(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )


def set_user_password(user_id: int, password: str):
    user = User.objects.get(pk=user_id)
    user.set_password(password)
    user.save()
    return user_dataclasses.User(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )


def get_or_create_user_group_by_name(name: str):
    user_group, _ = Group.objects.get_or_create(name=name)
    return user_dataclasses.UserGroup(id=user_group.id, name=user_group.name)


def set_user_groups(user_id: int, group_ids: list[int]):
    user = User.objects.get(pk=user_id)
    user.groups.set(group_ids)
    user.save()


def add_user_group(user_id: int, group_id: int):
    user = User.objects.get(pk=user_id)
    user.groups.add(group_id)
    user.save()
