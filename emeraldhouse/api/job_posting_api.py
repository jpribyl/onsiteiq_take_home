from rest_framework import serializers

from emeraldhouse.models import job_posting_models


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = job_posting_models.JobPosting
        fields = ["title"]
