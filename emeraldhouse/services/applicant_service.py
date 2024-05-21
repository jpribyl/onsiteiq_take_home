from emeraldhouse.dal import applicant_dal, user_dal, job_posting_dal


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

    return applicant_dal.create(
        user_id=user.id,
        job_posting_id=job_posting.id,
    )
