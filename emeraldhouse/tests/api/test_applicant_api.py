import pytest

from emeraldhouse.models import applicant_models
from emeraldhouse.permissions import permission_constants
from emeraldhouse.services import permission_service
from emeraldhouse.tests import factories


def test_list_applicants_includes_applicant(user_full_access_client, applicant):
    response = user_full_access_client.get("/applicants/")
    applicants = response.json()
    assert response.status_code == 200
    assert len(applicants) == 1
    assert applicants[0]["id"] == applicant.id
    assert applicants[0]["user"]["first_name"] == applicant.user.first_name
    assert applicants[0]["user"]["last_name"] == applicant.user.last_name


def test_list_applicants_includes_default_applicant_state(
    user_full_access_client, applicant
):
    response = user_full_access_client.get("/applicants/")
    applicants = response.json()
    expected_applicant_state = applicant_models.ApplicantState.ApplicantStates.PENDING
    assert applicants[0]["applicant_state"] == expected_applicant_state


def test_view_applicant(user_no_access, user_no_access_client, applicant):
    response = user_no_access_client.get(f"/applicants/{applicant.id}/")
    assert response.status_code == 403
    permission_service.add_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant.id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.applicant,
        permission_codename=permission_constants.ObjectPermissions.applicant_view,
    )
    response = user_no_access_client.get(f"/applicants/{applicant.id}/")
    assert response.status_code == 200

    new_job_applicant = factories.ApplicantFactory()
    response = user_no_access_client.get(f"/applicants/{new_job_applicant.id}/")
    assert response.status_code == 403

    same_job_applicant = factories.ApplicantFactory(job_posting=applicant.job_posting)
    response = user_no_access_client.get(f"/applicants/{same_job_applicant.id}/")
    assert response.status_code == 403


def test_view_job_posting_applicant(user_no_access, user_no_access_client, applicant):
    response = user_no_access_client.get(f"/applicants/{applicant.id}/")
    assert response.status_code == 403
    permission_service.add_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant.job_posting_id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.job_posting,
        permission_codename=permission_constants.ObjectPermissions.applicant_view,
    )
    response = user_no_access_client.get(f"/applicants/{applicant.id}/")
    assert response.status_code == 200

    new_job_applicant = factories.ApplicantFactory()
    response = user_no_access_client.get(f"/applicants/{new_job_applicant.id}/")
    assert response.status_code == 403

    same_job_applicant = factories.ApplicantFactory(job_posting=applicant.job_posting)
    response = user_no_access_client.get(f"/applicants/{same_job_applicant.id}/")
    assert response.status_code == 200


def test_transition_state_updates_application_state(user_full_access_client, applicant):
    expected_applicant_state = applicant_models.ApplicantState.ApplicantStates.APPROVED
    user_full_access_client.post(
        f"/applicants/{applicant.id}/transition_applicant/",
        data={"state": expected_applicant_state},
        content_type="application/json",
    )
    response = user_full_access_client.get("/applicants/")
    applicants = response.json()
    assert applicants[0]["applicant_state"] == expected_applicant_state


def test_create_applicant(user_full_access_client):
    user_data = {
        "first_name": "larry",
        "last_name": "smith",
        "email": "larry@smith.com",
    }
    job_posting_data = {"title": "engineer"}
    response = user_full_access_client.post(
        "/applicants/",
        data={"user": user_data, "job_posting": job_posting_data},
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json()["user"] == user_data
    response = user_full_access_client.get("/applicants/")
    assert len(response.json()) == 1
    applicant = response.json()[0]
    assert (
        applicant["applicant_state"]
        == applicant_models.ApplicantState.ApplicantStates.PENDING.value
    )


def test_delete_applicant_not_possible(user_full_access_client, applicant):
    response = user_full_access_client.delete(
        f"/applicants/{applicant.id}/",
    )
    assert response.status_code == 405


def test_create_applicant_note(
    user_full_access_client,
    applicant,
    user_no_access,
    user_no_access_client,
):
    note_text = "applicant note text"
    response = user_full_access_client.post(
        f"/applicants/{applicant.id}/add_note/",
        data={"text": note_text},
        content_type="application/json",
    )
    assert response.status_code == 201

    response = user_full_access_client.get(f"/applicant_notes/")
    assert len(response.json()) == 1
    applicant_note = response.json()[0]
    assert applicant_note["text"] == note_text

    permission_service.add_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant.id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.applicant,
        permission_codename=permission_constants.ObjectPermissions.applicant_note_add,
    )
    note_text = "applicant note text"
    response = user_no_access_client.post(
        f"/applicants/{applicant.id}/add_note/",
        data={"text": note_text},
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json()["text"] == note_text


def test_create_job_posting_applicant_note(
    user_no_access, user_no_access_client, applicant
):
    permission_service.add_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant.job_posting_id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.job_posting,
        permission_codename=permission_constants.ObjectPermissions.applicant_note_add,
    )
    note_text = "applicant note text"
    response = user_no_access_client.post(
        f"/applicants/{applicant.id}/add_note/",
        data={"text": note_text},
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json()["text"] == note_text


def test_view_applicant_notes(user_no_access, user_no_access_client, applicant_note):
    response = user_no_access_client.get(
        f"/applicants/{applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 403
    permission_service.add_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant_note.applicant.id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.applicant,
        permission_codename=permission_constants.ObjectPermissions.applicant_note_view,
    )
    response = user_no_access_client.get(
        f"/applicants/{applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 200

    second_applicant_note = factories.ApplicantNoteFactory(
        applicant=applicant_note.applicant
    )
    response = user_no_access_client.get(
        f"/applicants/{second_applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert set(note["id"] for note in response.json()) == set(
        [applicant_note.id, second_applicant_note.id]
    )

    same_job_applicant = factories.ApplicantFactory(
        job_posting=applicant_note.applicant.job_posting
    )
    same_job_applicant_note = factories.ApplicantNoteFactory(
        applicant=same_job_applicant
    )
    response = user_no_access_client.get(
        f"/applicants/{same_job_applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 403


def test_view_job_posting_applicant_notes(
    user_no_access, user_no_access_client, applicant_note
):
    response = user_no_access_client.get(
        f"/applicants/{applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 403
    permission_service.add_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant_note.applicant.job_posting_id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.job_posting,
        permission_codename=permission_constants.ObjectPermissions.applicant_note_view,
    )
    response = user_no_access_client.get(
        f"/applicants/{applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 200

    second_applicant_note = factories.ApplicantNoteFactory(
        applicant=applicant_note.applicant
    )
    response = user_no_access_client.get(
        f"/applicants/{second_applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 200

    same_job_applicant = factories.ApplicantFactory(
        job_posting=applicant_note.applicant.job_posting
    )
    same_job_applicant_note = factories.ApplicantNoteFactory(
        applicant=same_job_applicant
    )
    response = user_no_access_client.get(
        f"/applicants/{same_job_applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 200

    new_job_applicant_note = factories.ApplicantNoteFactory()
    response = user_no_access_client.get(
        f"/applicants/{new_job_applicant_note.applicant.id}/view_notes/"
    )
    assert response.status_code == 403


@pytest.mark.parametrize(
    "endpoint,expected_status_code",
    [
        ("/applicants/", 403),
        ("/applicants/1/", 404),
        ("/applicants/1/transition_applicant/", 405),
        ("/applicant_notes/", 403),
        ("/applicant_notes/1/", 404),
    ],
)
def test_get_status_codes(user_no_access_client, endpoint, expected_status_code):
    response = user_no_access_client.get(endpoint)
    assert response.status_code == expected_status_code
