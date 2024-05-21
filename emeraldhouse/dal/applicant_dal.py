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
