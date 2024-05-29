import pytest
from django.contrib.auth import models as django_contrib_auth_models

from emeraldhouse.models import applicant_models, job_posting_models
from emeraldhouse.services import applicant_service

APPLICANT_DATA = {
    "first_name": "first",
    "last_name": "last",
    "email": "first@last.com",
    "job_posting_title": "engineer level 1",
}


@pytest.mark.django_db
def test_apply_to_job_posting_creates_user():
    applicant = applicant_service.apply_to_job_posting(**APPLICANT_DATA)
    user = django_contrib_auth_models.User.objects.get(id=applicant.user_id)
    assert user.first_name == APPLICANT_DATA["first_name"]
    assert user.last_name == APPLICANT_DATA["last_name"]
    assert user.email == APPLICANT_DATA["email"]


@pytest.mark.django_db
def test_apply_to_job_posting_creates_applicant():
    applicant = applicant_service.apply_to_job_posting(**APPLICANT_DATA)
    assert applicant_models.Applicant.objects.filter(id=applicant.id).exists()


@pytest.mark.django_db
def test_apply_to_job_posting_links_job_posting():
    applicant = applicant_service.apply_to_job_posting(**APPLICANT_DATA)
    job_posting = job_posting_models.JobPosting.objects.get(id=applicant.job_posting_id)
    assert job_posting.title == APPLICANT_DATA["job_posting_title"]
    assert (
        job_posting
        == applicant_models.Applicant.objects.get(id=applicant.id).job_posting
    )


@pytest.mark.django_db
def test_apply_to_job_posting_sets_pending_applicant_state():
    applicant = applicant_service.apply_to_job_posting(**APPLICANT_DATA)
    applicant_transitions = applicant_models.ApplicantTransition.objects.filter(
        applicant_id=applicant.id
    )
    assert len(applicant_transitions) == 1
    assert (
        applicant_transitions[0].applicant_state.state
        == applicant_models.ApplicantState.ApplicantStates.PENDING
    )


@pytest.mark.django_db
def test_apply_to_job_posting_allows_applicant_to_submit_twice():
    applicant_1 = applicant_service.apply_to_job_posting(**APPLICANT_DATA)
    applicant_2 = applicant_service.apply_to_job_posting(**APPLICANT_DATA)

    assert applicant_1.user_id == applicant_2.user_id
    assert applicant_1.job_posting_id == applicant_2.job_posting_id
    assert applicant_1.id != applicant_2.id

    applicant_states = applicant_models.ApplicantState.objects.all()
    assert len(applicant_states) == 1


@pytest.mark.django_db
def test_update_applicant_state_fails_with_fake_state(applicant):
    with pytest.raises(ValueError):
        applicant_service.update_applicant_state(
            applicant_id=applicant.id, state="FAKE STATE"
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "applicant_state",
    [
        applicant_models.ApplicantState.ApplicantStates.APPROVED,
        applicant_models.ApplicantState.ApplicantStates.REJECTED,
        applicant_models.ApplicantState.ApplicantStates.PENDING,
    ],
)
def test_update_applicant_state_succeeds(applicant, applicant_state):
    applicant_service.update_applicant_state(
        applicant_id=applicant.id,
        state=applicant_state,
    )

    # TODO: this query is the same as the subquery in the applicant_api, it really
    # ought to be moved to a re-usable layer and explicitly tested
    latest_state = (
        applicant_models.ApplicantTransition.objects.filter(applicant_id=applicant.id)
        .select_related("applicant_state")
        .order_by("-transitioned_at")
        .values("applicant_state__state")[0]["applicant_state__state"]
    )
    assert latest_state == applicant_state
