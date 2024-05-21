from django.contrib.auth.models import User

from emeraldhouse.dataclasses import user_dataclasses


def get_or_create(
    first_name: str,
    last_name: str,
    email: str,
) -> user_dataclasses.CreatedUser:
    user, _ = User.objects.get_or_create(
        username=email,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    return user_dataclasses.CreatedUser(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )
