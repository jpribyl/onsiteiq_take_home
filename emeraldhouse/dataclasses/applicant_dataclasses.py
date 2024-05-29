import dataclasses
from datetime import datetime


@dataclasses.dataclass
class CreatedApplicant:
    id: int
    user_id: int
    job_posting_id: int


@dataclasses.dataclass
class ApplicantState:
    id: int
    state: str


@dataclasses.dataclass
class ApplicantTransition:
    id: int
    transitioned_at: datetime


@dataclasses.dataclass
class ApplicantTransitionState:
    transition: ApplicantTransition
    state: ApplicantState


@dataclasses.dataclass
class ApplicantNote:
    id: int
    applicant_id: int
    user_id: int
    text: str
