from django.contrib.auth import models as django_contrib_auth_models

from emeraldhouse.services import user_service


def test_get_or_create_user(user_no_access):
    assert len(django_contrib_auth_models.User.objects.all()) == 1
    user_service.get_or_create_user(
        first_name=user_no_access.first_name,
        last_name=user_no_access.last_name,
        email=user_no_access.email,
    )
    assert len(django_contrib_auth_models.User.objects.all()) == 1

    user_service.get_or_create_user(
        first_name=user_no_access.first_name,
        last_name=user_no_access.last_name,
        email="new_user_email@mail.com",
    )
    assert len(django_contrib_auth_models.User.objects.all()) == 2


def test_set_user_password(user_no_access):
    new_password = "new_password"
    user_service.set_user_password(user_id=user_no_access.id, password=new_password)
    user_no_access.refresh_from_db()
    assert user_no_access.check_password(new_password)


def test_add_user_group(user_no_access):
    group_name_1 = "new_group_1"
    assert len(django_contrib_auth_models.Group.objects.all()) == 0
    assert len(user_no_access.groups.all()) == 0
    user_service.add_user_group(user_id=user_no_access.id, group_name=group_name_1)
    assert len(django_contrib_auth_models.Group.objects.all()) == 1
    assert len(user_no_access.groups.all()) == 1
    assert user_no_access.groups.filter(name=group_name_1).exists()

    user_service.add_user_group(user_id=user_no_access.id, group_name=group_name_1)
    assert len(django_contrib_auth_models.Group.objects.all()) == 1
    assert len(user_no_access.groups.all()) == 1
    assert user_no_access.groups.filter(name=group_name_1).exists()

    group_name_2 = "new_group_2"
    user_service.add_user_group(user_id=user_no_access.id, group_name=group_name_2)
    assert len(django_contrib_auth_models.Group.objects.all()) == 2
    assert len(user_no_access.groups.all()) == 2
    assert user_no_access.groups.filter(name=group_name_1).exists()
    assert user_no_access.groups.filter(name=group_name_2).exists()


def test_set_user_groups(user_no_access):
    group_names_1 = ["new_group_1", "new_group_2"]
    user_service.set_user_groups(user_id=user_no_access.id, group_names=group_names_1)
    assert len(django_contrib_auth_models.Group.objects.all()) == 2
    assert len(user_no_access.groups.all()) == 2
    for group_name in group_names_1:
        assert user_no_access.groups.filter(name=group_name).exists()

    group_names_2 = ["new_group_3", "new_group_4"]
    user_service.set_user_groups(user_id=user_no_access.id, group_names=group_names_2)
    assert len(django_contrib_auth_models.Group.objects.all()) == 4
    assert len(user_no_access.groups.all()) == 2
    for group_name in group_names_2:
        assert user_no_access.groups.filter(name=group_name).exists()
