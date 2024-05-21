from rest_framework import serializers, viewsets
from emeraldhouse.api import auth_user_api
from emeraldhouse.api import job_posting_api
from emeraldhouse.models import applicant_models
from emeraldhouse.services import applicant_service


class ApplicantSerializer(serializers.ModelSerializer):
    user = auth_user_api.WebSafeUserSerializer()
    job_posting = job_posting_api.JobPostingSerializer()

    class Meta:
        model = applicant_models.Applicant
        fields = ["user", "job_posting"]

    # Left in to demonstrate how DRF serializers *may* be used to hold business
    # logic if separating app layers from framework is not a concern
    #
    #
    # def create(self, validated_data):
    #   user_data = validated_data.pop("user")
    #   user_email = user_data.pop("email")
    #   user, created = User.objects.get_or_create(
    #       username=user_email,
    #       email=user_email,
    #       defaults=user_data,
    #   )

    #   job_posting_data = validated_data.pop("job_posting")
    #   job_posting_title = job_posting_data.pop("title")
    #   job_posting, created = JobPosting.objects.get_or_create(
    #       title=job_posting_title,
    #       defaults=job_posting_data,
    #   )

    #   validated_data["user_id"] = user.id
    #   validated_data["job_posting_id"] = job_posting.id

    #   return super().create(validated_data)


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = applicant_models.Applicant.objects.select_related(
        "user",
        "job_posting",
    ).all()
    serializer_class = ApplicantSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        applicant_service.apply_to_job_posting(
            first_name=validated_data["user"]["first_name"],
            last_name=validated_data["user"]["last_name"],
            email=validated_data["user"]["email"],
            job_posting_title=validated_data["job_posting"]["title"],
        )
