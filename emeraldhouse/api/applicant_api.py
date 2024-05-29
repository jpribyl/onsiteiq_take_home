from django.db import models as django_models
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import response as rest_framework_response
from rest_framework import serializers, viewsets
from rest_framework.decorators import action

from emeraldhouse.api import auth_user_api, job_posting_api
from emeraldhouse.models import applicant_models
from emeraldhouse.permissions import applicant_rules, permission_mixins
from emeraldhouse.services import applicant_service


class ApplicantSerializer(serializers.ModelSerializer[applicant_models.Applicant]):
    user = auth_user_api.WebSafeUserSerializer()
    job_posting = job_posting_api.JobPostingSerializer()
    applicant_state = serializers.SerializerMethodField()

    class Meta:
        model = applicant_models.Applicant
        fields = ["id", "user", "job_posting", "applicant_state"]

    def get_applicant_state(self, obj):
        try:
            return obj.applicant_state

        # outbound domain objects have applicant_state but inbound are dicts
        # and will not be dot-indexable
        #
        # TODO: simplify inbound / outbound parsing
        except AttributeError:
            return None

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


class ApplicantTransitionSerializer(serializers.Serializer):
    state = serializers.ChoiceField(
        choices=applicant_models.ApplicantState.ApplicantStates
    )


class ApplicantNoteSerializer(
    serializers.ModelSerializer[applicant_models.ApplicantNote]
):
    applicant_id = serializers.IntegerField()

    class Meta:
        model = applicant_models.ApplicantNote
        fields = [
            "id",
            "created_at",
            "updated_at",
            "text",
            "user_id",
            "applicant_id",
        ]

    def get_current_user_id(self):
        return self.context["request"].user.id


class ApplicantViewSet(
    permission_mixins.CustomAutoPermissionViewSetMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):

    # It's a bit of a code smell to access models directly here instead of
    # through a DAL & service layer. This is one of the most common criticisms
    # of class-based Django / DRF
    queryset = (
        applicant_models.Applicant.objects.select_related(
            "user",
            "job_posting",
        )
        .annotate(
            applicant_state=django_models.Subquery(
                applicant_models.ApplicantTransition.objects.filter(
                    applicant_id=django_models.OuterRef("id")
                )
                .select_related("applicant_state")
                .order_by("-transitioned_at")
                .values("applicant_state__state")[:1]
            )
        )
        .all()
    )

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        applicant_service.apply_to_job_posting(
            first_name=validated_data["user"]["first_name"],
            last_name=validated_data["user"]["last_name"],
            email=validated_data["user"]["email"],
            job_posting_title=validated_data["job_posting"]["title"],
        )

    def get_serializer_class(self):
        if self.action == "transition_applicant":
            return ApplicantTransitionSerializer
        if self.action in ["add_note", "view_notes"]:
            return ApplicantNoteSerializer
        return ApplicantSerializer

    @extend_schema(
        description="Allows the user to transition an applicant from one state (PENDING for example) to another (APPROVED for example) in an auditable manner",
    )
    @action(detail=True, methods=["post"])
    def transition_applicant(self, request, pk):
        applicant_id = pk
        state = request.data["state"]
        applicant_transition_state = applicant_service.update_applicant_state(
            applicant_id=applicant_id,
            state=state,
        )
        serializer = self.get_serializer(applicant_transition_state.state)
        return rest_framework_response.Response(serializer.data)

    @extend_schema(
        description="Allows the user to add a note to an applicant",
    )
    @action(detail=True, methods=["post"])
    def add_note(self, request, pk):
        applicant_id = pk
        text = request.data["text"]
        applicant_note = applicant_service.create_applicant_note(
            user_id=request.user.id,
            applicant_id=applicant_id,
            text=text,
        )
        serializer = self.get_serializer(applicant_note)
        return rest_framework_response.Response(serializer.data, status=201)

    @extend_schema(
        description="Allows the user to add a note to an applicant",
    )
    @action(detail=True, methods=["get"])
    def view_notes(self, request, pk):
        applicant_id = pk
        applicant_note = applicant_service.get_notes_for_applicant(
            applicant_id=applicant_id
        )
        serializer = self.get_serializer(applicant_note, many=True)
        return rest_framework_response.Response(serializer.data)


class ApplicantNoteViewSet(
    permission_mixins.CustomAutoPermissionViewSetMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = applicant_models.ApplicantNote.objects.all()
    serializer_class = ApplicantNoteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        applicant_service.create_applicant_note(
            user_id=serializer.context["request"].user.id,
            applicant_id=validated_data["applicant_id"],
            text=validated_data["text"],
        )
