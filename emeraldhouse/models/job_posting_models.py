from django.contrib.auth import models as django_contrib_auth_models
from django.db import models


class JobPosting(models.Model):
    title = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewers = models.ManyToManyField(
        django_contrib_auth_models.User,
        related_name="job_posting_viewer",
    )
    editors = models.ManyToManyField(
        django_contrib_auth_models.User,
        related_name="job_posting_editor",
    )
