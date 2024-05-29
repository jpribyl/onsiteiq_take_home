import rules

from emeraldhouse.permissions import permission_constants
from emeraldhouse.services import permission_service


def _verify_applicant_permission(permission_codename):
    @rules.predicate
    def rule_predicate(user, applicant):
        return permission_service.verify_user_object_permission(
            user_id=user.id,
            object_id=applicant.id,
            app_label=permission_constants.AppLabels.emeraldhouse,
            model=permission_constants.ModelNames.applicant,
            permission_codename=permission_codename,
        )

    return rule_predicate


def _verify_job_posting_applicant_permission(permission_codename):
    @rules.predicate
    def rule_predicate(user, applicant):
        return permission_service.verify_user_object_permission(
            user_id=user.id,
            object_id=applicant.job_posting_id,
            app_label=permission_constants.AppLabels.emeraldhouse,
            model=permission_constants.ModelNames.job_posting,
            permission_codename=permission_codename,
        )

    return rule_predicate


############################
# APPLICANT VIEW PERMISSIONS
############################
can_view_applicant = _verify_applicant_permission(
    permission_constants.ObjectPermissions.applicant_view
)
can_view_job_posting_applicants = _verify_job_posting_applicant_permission(
    permission_constants.ObjectPermissions.applicant_view
)
can_view_all_applicants = rules.is_group_member(
    permission_constants.Groups.applicant_view_all
)


##############################
# APPLICANT CREATE PERMISSIONS
##############################
can_add_all_applicants = rules.is_group_member(
    permission_constants.Groups.applicant_add_all
)

##############################
# APPLICANT UPDATE PERMISSIONS
##############################
can_change_applicant = _verify_applicant_permission(
    permission_constants.ObjectPermissions.applicant_change
)
can_change_job_posting_applicants = _verify_job_posting_applicant_permission(
    permission_constants.ObjectPermissions.applicant_change
)
can_change_all_applicants = rules.is_group_member(
    permission_constants.Groups.applicant_change_all
)

#################################
# APPLICANT NOTE VIEW PERMISSIONS
#################################
can_view_applicant_note = _verify_applicant_permission(
    permission_constants.ObjectPermissions.applicant_note_view
)
can_view_job_posting_applicant_notes = _verify_job_posting_applicant_permission(
    permission_constants.ObjectPermissions.applicant_note_view
)
can_view_all_applicant_notes = rules.is_group_member(
    permission_constants.Groups.applicant_note_view_all
)

###################################
# APPLICANT NOTE CREATE PERMISSIONS
###################################

can_add_applicant_note = _verify_applicant_permission(
    permission_constants.ObjectPermissions.applicant_note_add
)

can_add_job_posting_applicant_notes = _verify_job_posting_applicant_permission(
    permission_constants.ObjectPermissions.applicant_note_add
)

can_add_all_applicant_notes = rules.is_group_member(
    permission_constants.Groups.applicant_note_add_all
)
