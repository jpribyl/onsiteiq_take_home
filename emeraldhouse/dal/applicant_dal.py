from datetime import datetime

from emeraldhouse.dataclasses import applicant_dataclasses
from emeraldhouse.models import applicant_models


def create(user_id: int, job_posting_id: int) -> applicant_dataclasses.CreatedApplicant:
    applicant = applicant_models.Applicant.objects.create(
        user_id=user_id,
        job_posting_id=job_posting_id,
    )

    return applicant_dataclasses.CreatedApplicant(
        id=applicant.id,
        user_id=applicant.user_id,
        job_posting_id=applicant.job_posting_id,
    )


def get_or_create_applicant_state(state: str):
    applicant_state, _ = applicant_models.ApplicantState.objects.get_or_create(
        state=applicant_models.ApplicantState.ApplicantStates(state)
    )
    return applicant_dataclasses.ApplicantState(
        id=applicant_state.id,
        state=applicant_state.state,
    )


def create_applicant_transition(
    applicant_id: int,
    applicant_state_id: int,
    transitioned_at: datetime,
):
    transition = applicant_models.ApplicantTransition.objects.create(
        applicant_id=applicant_id,
        applicant_state_id=applicant_state_id,
        transitioned_at=transitioned_at,
    )
    return applicant_dataclasses.ApplicantTransition(
        id=transition.id,
        transitioned_at=transitioned_at,
    )


def create_applicant_note(applicant_id: int, user_id: int, text: str):
    note = applicant_models.ApplicantNote.objects.create(
        applicant_id=applicant_id,
        user_id=user_id,
        text=text,
    )
    return applicant_dataclasses.ApplicantNote(
        id=note.id,
        applicant_id=note.applicant_id,
        user_id=note.user_id,
        text=note.text,
    )


def get_notes_for_applicant(applicant_id: int):
    notes = applicant_models.ApplicantNote.objects.filter(
        applicant_id=applicant_id,
    )
    return [
        applicant_dataclasses.ApplicantNote(
            id=note.id,
            applicant_id=note.applicant_id,
            user_id=note.user_id,
            text=note.text,
        )
        for note in notes
    ]
