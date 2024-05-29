from emeraldhouse.dal import user_dal


def get_or_create_user(
    first_name: str,
    last_name: str,
    email: str,
):
    return user_dal.get_or_create(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )


def set_user_password(user_id: int, password: str):
    return user_dal.set_user_password(user_id=user_id, password=password)


def set_user_groups(user_id: int, group_names: list[str]):
    # TODO: optimize queries- this is only used by a mangaement command
    # presently so it is not a high priority
    group_ids = [
        user_dal.get_or_create_user_group_by_name(name=name).id for name in group_names
    ]
    return user_dal.set_user_groups(user_id=user_id, group_ids=group_ids)


def add_user_group(user_id: int, group_name: str):
    group_id = user_dal.get_or_create_user_group_by_name(name=group_name).id
    return user_dal.add_user_group(user_id=user_id, group_id=group_id)
