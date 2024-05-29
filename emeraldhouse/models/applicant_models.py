import rules.contrib.models as rules_models
from django.contrib.auth import models as django_contrib_auth_models
from django.db import models

from emeraldhouse.models import job_posting_models
from emeraldhouse.permissions import applicant_rules


class Applicant(rules_models.RulesModel):
    class Meta:
        rules_permissions = {
            "list": applicant_rules.can_view_all_applicants,
            "view": applicant_rules.can_view_all_applicants
            | applicant_rules.can_view_applicant
            | applicant_rules.can_view_job_posting_applicants,
            "change": applicant_rules.can_change_all_applicants
            | applicant_rules.can_change_applicant
            | applicant_rules.can_change_job_posting_applicants,
            "add": applicant_rules.can_add_all_applicants,
            "add_note": applicant_rules.can_add_all_applicant_notes
            | applicant_rules.can_add_applicant_note
            | applicant_rules.can_add_job_posting_applicant_notes,
            "view_notes": applicant_rules.can_view_all_applicant_notes
            | applicant_rules.can_view_applicant_note
            | applicant_rules.can_view_job_posting_applicant_notes,
        }

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
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"

    state = models.CharField(choices=ApplicantStates)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApplicantTransition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transitioned_at = models.DateTimeField(blank=False, null=False)
    applicant_state = models.ForeignKey(ApplicantState, on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        Applicant,
        on_delete=models.CASCADE,
        related_name="applicant_transitions",
    )


class ApplicantNote(rules_models.RulesModel):
    class Meta:
        rules_permissions = {
            "list": applicant_rules.can_view_all_applicant_notes,
        }

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
