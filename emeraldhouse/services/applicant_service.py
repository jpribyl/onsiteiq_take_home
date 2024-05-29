from datetime import datetime

import pytz

from emeraldhouse.dal import applicant_dal, job_posting_dal, user_dal
from emeraldhouse.dataclasses import applicant_dataclasses
from emeraldhouse.models import applicant_models


def apply_to_job_posting(
    first_name: str,
    last_name: str,
    email: str,
    job_posting_title: str,
):
    user = user_dal.get_or_create(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    job_posting = job_posting_dal.get_or_create(
        title=job_posting_title,
    )

    applicant = applicant_dal.create(
        user_id=user.id,
        job_posting_id=job_posting.id,
    )

    default_applicant_state = applicant_dal.get_or_create_applicant_state(
        applicant_models.ApplicantState.ApplicantStates.PENDING
    )
    applicant_dal.create_applicant_transition(
        applicant_id=applicant.id,
        applicant_state_id=default_applicant_state.id,
        transitioned_at=datetime.now(pytz.utc),
    )
    return applicant


def update_applicant_state(applicant_id: int, state: str):
    transitioned_at = datetime.now(pytz.utc)
    applicant_state = applicant_dal.get_or_create_applicant_state(state=state)
    applicant_transition = applicant_dal.create_applicant_transition(
        applicant_id=applicant_id,
        applicant_state_id=applicant_state.id,
        transitioned_at=transitioned_at,
    )
    return applicant_dataclasses.ApplicantTransitionState(
        state=applicant_state,
        transition=applicant_transition,
    )


def create_applicant_note(applicant_id: int, user_id: int, text: str):
    return applicant_dal.create_applicant_note(
        applicant_id=applicant_id,
        user_id=user_id,
        text=text,
    )


def get_notes_for_applicant(applicant_id: int):
    return applicant_dal.get_notes_for_applicant(
        applicant_id=applicant_id,
    )
