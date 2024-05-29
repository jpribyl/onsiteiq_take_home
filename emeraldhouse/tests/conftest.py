import pytest
from django.test import Client

from emeraldhouse.permissions import utils as permission_utils
from emeraldhouse.tests import factories


@pytest.fixture
def user_no_access(django_user_model):
    return django_user_model.objects.create_user(
        username="test_user_no_access@mail.com",
        password="password",
        email="test_user_no_access@mail.com",
    )


@pytest.fixture
def user_full_access(django_user_model):
    user = django_user_model.objects.create_user(
        username="test_user_view_all@mail.com",
        password="password",
        email="test_user_view_all@mail.com",
    )

    permission_utils.allow_user_full_applicant_access(user)
    return user


@pytest.fixture
def user_no_access_client(user_no_access):
    access_token = permission_utils.get_tokens_for_user(user_no_access)["access"]
    return Client(headers={"Authorization": f"Bearer {access_token}"})


@pytest.fixture
def user_full_access_client(user_full_access):
    access_token = permission_utils.get_tokens_for_user(user_full_access)["access"]
    return Client(headers={"Authorization": f"Bearer {access_token}"})


@pytest.fixture
def applicant():
    return factories.ApplicantFactory()


@pytest.fixture
def applicant_note():
    return factories.ApplicantNoteFactory()
