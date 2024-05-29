from rest_framework_simplejwt import tokens as simplejwt_tokens

from emeraldhouse.permissions import permission_constants
from emeraldhouse.services import permission_service, user_service


def create_user_applicant_permission(
    user_id,
    applicant_id,
    permission_codename=permission_constants.ObjectPermissions.applicant_view,
):
    permission_service.add_user_object_permission(
        user_id=user_id,
        object_id=applicant_id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.applicant,
        permission_codename=permission_codename,
    )


def create_user_job_posting_applicant_permission(
    user_id,
    job_posting_id,
    permission_codename=permission_constants.ObjectPermissions.applicant_view,
):
    permission_service.add_user_object_permission(
        user_id=user_id,
        object_id=job_posting_id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.job_posting,
        permission_codename=permission_codename,
    )


def create_user_applicant_note_permission(
    user_id,
    applicant_id,
    permission_codename=permission_constants.ObjectPermissions.applicant_view,
):
    permission_service.add_user_object_permission(
        user_id=user_id,
        object_id=applicant_id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.applicant,
        permission_codename=permission_codename,
    )


def create_user_job_posting_applicant_note_permission(
    user_id,
    job_posting_id,
    permission_codename=permission_constants.ObjectPermissions.applicant_view,
):
    permission_service.add_user_object_permission(
        user_id=user_id,
        object_id=job_posting_id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.job_posting,
        permission_codename=permission_codename,
    )


def allow_user_full_applicant_access(user):
    user_service.add_user_group(
        user_id=user.id,
        group_name=permission_constants.Groups.applicant_view_all,
    )
    user_service.add_user_group(
        user_id=user.id,
        group_name=permission_constants.Groups.applicant_add_all,
    )
    user_service.add_user_group(
        user_id=user.id,
        group_name=permission_constants.Groups.applicant_change_all,
    )
    user_service.add_user_group(
        user_id=user.id,
        group_name=permission_constants.Groups.applicant_note_add_all,
    )
    user_service.add_user_group(
        user_id=user.id,
        group_name=permission_constants.Groups.applicant_note_view_all,
    )


def get_tokens_for_user(user):
    refresh = simplejwt_tokens.RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
