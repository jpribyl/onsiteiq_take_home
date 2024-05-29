import pytest

from emeraldhouse.permissions import permission_constants
from emeraldhouse.services import permission_service


@pytest.mark.parametrize(
    "permission_codename",
    [
        permission_constants.ObjectPermissions.applicant_add,
        permission_constants.ObjectPermissions.applicant_view,
        permission_constants.ObjectPermissions.applicant_change,
        permission_constants.ObjectPermissions.applicant_note_add,
        permission_constants.ObjectPermissions.applicant_note_view,
    ],
)
def test_verify_user_object_missing_permission(
    user_no_access, applicant, permission_codename
):
    has_permission = permission_service.verify_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant.id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.applicant,
        permission_codename=permission_codename,
    )
    assert has_permission == False


@pytest.mark.parametrize(
    "permission_codename",
    [
        permission_constants.ObjectPermissions.applicant_add,
        permission_constants.ObjectPermissions.applicant_view,
        permission_constants.ObjectPermissions.applicant_change,
        permission_constants.ObjectPermissions.applicant_note_add,
        permission_constants.ObjectPermissions.applicant_note_view,
    ],
)
def test_verify_user_object_add_permission(
    user_no_access, applicant, permission_codename
):
    permission_service.add_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant.id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.applicant,
        permission_codename=permission_codename,
    )
    has_permission = permission_service.verify_user_object_permission(
        user_id=user_no_access.id,
        object_id=applicant.id,
        app_label=permission_constants.AppLabels.emeraldhouse,
        model=permission_constants.ModelNames.applicant,
        permission_codename=permission_codename,
    )
    assert has_permission == True
