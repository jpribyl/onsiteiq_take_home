import dataclasses


@dataclasses.dataclass
class CreatedApplicant:
    id: int
    user_id: int
    job_posting_id: int
