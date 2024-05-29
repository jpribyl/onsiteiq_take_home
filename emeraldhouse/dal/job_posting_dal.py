from emeraldhouse.dataclasses import job_posting_dataclasses
from emeraldhouse.models import job_posting_models


def get_or_create(title: str) -> job_posting_dataclasses.CreatedJobPosting:
    job_posting, _ = job_posting_models.JobPosting.objects.get_or_create(title=title)
    return job_posting_dataclasses.CreatedJobPosting(
        id=job_posting.id,
        title=job_posting.title,
    )
