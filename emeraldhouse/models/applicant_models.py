from django.db import models
from django.contrib.auth import models as django_contrib_auth_models
from emeraldhouse.models import job_posting_models


class Applicant(models.Model):
    user = models.ForeignKey(
        django_contrib_auth_models.User,
        on_delete=models.CASCADE,
    )
    job_posting = models.ForeignKey(
        job_posting_models.JobPosting,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApplicantState(models.Model):
    class ApplicantStates(models.TextChoices):
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"

    state = models.CharField(choices=ApplicantStates)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApplicantTransition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transitioned_at = models.DateTimeField(blank=False, null=False)
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        related_name="applicant_transitions",
    )


class ApplicantNote(models.Model):
    user = models.ForeignKey(
        django_contrib_auth_models.User,
        on_delete=models.CASCADE,
    )
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
