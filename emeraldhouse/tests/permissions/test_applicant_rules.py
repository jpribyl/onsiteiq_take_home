from emeraldhouse.permissions import applicant_rules, permission_constants
from emeraldhouse.permissions import utils as permission_utils
from emeraldhouse.services import permission_service, user_service
from emeraldhouse.tests import factories

# TODO: it would be really nice to parametrize these so that it reads more like
# a truth-table


############################
# APPLICANT VIEW PERMISSIONS
############################
def test_view_all_applicants(user_no_access):
    user_service.add_user_group(
        user_id=user_no_access.id,
        group_name=permission_constants.Groups.applicant_view_all,
    )
    assert applicant_rules.can_view_all_applicants(user_no_access) == True


def test_view_job_posting_applicants(user_no_access, applicant):
    permission_utils.create_user_job_posting_applicant_permission(
        user_id=user_no_access.id,
        job_posting_id=applicant.job_posting_id,
        permission_codename=permission_constants.ObjectPermissions.applicant_view,
    )
    can_user_view = applicant_rules.can_view_job_posting_applicants(
        user=user_no_access, applicant=applicant
    )
    assert can_user_view == True

    second_applicant = factories.ApplicantFactory(
        job_posting_id=applicant.job_posting_id
    )
    can_user_view = applicant_rules.can_view_job_posting_applicants(
        user=user_no_access,
        applicant=second_applicant,
    )
    assert can_user_view == True

    new_job_posting_applicant = factories.ApplicantFactory()
    can_user_view = applicant_rules.can_view_job_posting_applicants(
        user=user_no_access,
        applicant=new_job_posting_applicant,
    )
    assert can_user_view == False


def test_view_applicant(user_no_access, applicant):
    permission_utils.create_user_applicant_permission(
        user_id=user_no_access.id,
        applicant_id=applicant.id,
        permission_codename=permission_constants.ObjectPermissions.applicant_view,
    )
    can_user_view = applicant_rules.can_view_applicant(
        user=user_no_access, applicant=applicant
    )
    assert can_user_view == True

    second_applicant = factories.ApplicantFactory(
        job_posting_id=applicant.job_posting_id
    )
    can_user_view = applicant_rules.can_view_applicant(
        user=user_no_access,
        applicant=second_applicant,
    )
    assert can_user_view == False

    new_job_posting_applicant = factories.ApplicantFactory()
    can_user_view = applicant_rules.can_view_applicant(
        user=user_no_access,
        applicant=new_job_posting_applicant,
    )
    assert can_user_view == False


##############################
# APPLICANT CREATE PERMISSIONS
##############################
def test_add_all_applicants(user_no_access):
    user_service.add_user_group(
        user_id=user_no_access.id,
        group_name=permission_constants.Groups.applicant_add_all,
    )
    assert applicant_rules.can_add_all_applicants(user_no_access) == True


##############################
# APPLICANT UPDATE PERMISSIONS
##############################
def test_change_all_applicants(user_no_access):
    user_service.add_user_group(
        user_id=user_no_access.id,
        group_name=permission_constants.Groups.applicant_change_all,
    )
    assert applicant_rules.can_change_all_applicants(user_no_access) == True


def test_change_job_posting_applicants(user_no_access, applicant):
    permission_utils.create_user_job_posting_applicant_permission(
        user_id=user_no_access.id,
        job_posting_id=applicant.job_posting_id,
        permission_codename=permission_constants.ObjectPermissions.applicant_change,
    )
    can_user_change = applicant_rules.can_change_job_posting_applicants(
        user=user_no_access, applicant=applicant
    )
    assert can_user_change == True

    second_applicant = factories.ApplicantFactory(
        job_posting_id=applicant.job_posting_id
    )
    can_user_change = applicant_rules.can_change_job_posting_applicants(
        user=user_no_access,
        applicant=second_applicant,
    )
    assert can_user_change == True

    new_job_posting_applicant = factories.ApplicantFactory()
    can_user_change = applicant_rules.can_change_job_posting_applicants(
        user=user_no_access,
        applicant=new_job_posting_applicant,
    )
    assert can_user_change == False


def test_change_applicant(user_no_access, applicant):
    permission_utils.create_user_applicant_permission(
        user_id=user_no_access.id,
        applicant_id=applicant.id,
        permission_codename=permission_constants.ObjectPermissions.applicant_change,
    )
    can_user_change = applicant_rules.can_change_applicant(
        user=user_no_access, applicant=applicant
    )
    assert can_user_change == True

    second_applicant = factories.ApplicantFactory(
        job_posting_id=applicant.job_posting_id
    )
    can_user_change = applicant_rules.can_change_applicant(
        user=user_no_access,
        applicant=second_applicant,
    )
    assert can_user_change == False

    new_job_posting_applicant = factories.ApplicantFactory()
    can_user_change = applicant_rules.can_change_applicant(
        user=user_no_access,
        applicant=new_job_posting_applicant,
    )
    assert can_user_change == False


#################################
# APPLICANT NOTE VIEW PERMISSIONS
#################################
def test_view_all_applicant_notes(user_no_access):
    user_service.add_user_group(
        user_id=user_no_access.id,
        group_name=permission_constants.Groups.applicant_note_view_all,
    )
    assert applicant_rules.can_view_all_applicant_notes(user_no_access) == True


def test_view_job_posting_applicant_notes(user_no_access, applicant):
    permission_utils.create_user_job_posting_applicant_note_permission(
        user_id=user_no_access.id,
        job_posting_id=applicant.job_posting.id,
        permission_codename=permission_constants.ObjectPermissions.applicant_note_view,
    )
    can_user_view = applicant_rules.can_view_job_posting_applicant_notes(
        user=user_no_access, applicant=applicant
    )
    assert can_user_view == True

    second_applicant = factories.ApplicantFactory(
        job_posting_id=applicant.job_posting_id
    )
    can_user_view = applicant_rules.can_view_job_posting_applicant_notes(
        user=user_no_access,
        applicant=second_applicant,
    )
    assert can_user_view == True

    new_job_posting_applicant = factories.ApplicantFactory()
    can_user_view = applicant_rules.can_view_job_posting_applicant_notes(
        user=user_no_access,
        applicant=new_job_posting_applicant,
    )
    assert can_user_view == False


def test_view_applicant_note(user_no_access, applicant):
    permission_utils.create_user_applicant_note_permission(
        user_id=user_no_access.id,
        applicant_id=applicant.id,
        permission_codename=permission_constants.ObjectPermissions.applicant_note_view,
    )
    can_user_view = applicant_rules.can_view_applicant_note(
        user=user_no_access, applicant=applicant
    )
    assert can_user_view == True

    second_applicant = factories.ApplicantFactory(
        job_posting_id=applicant.job_posting_id
    )
    can_user_view = applicant_rules.can_view_applicant_note(
        user=user_no_access,
        applicant=second_applicant,
    )
    assert can_user_view == False

    new_job_posting_applicant = factories.ApplicantFactory()
    can_user_view = applicant_rules.can_view_applicant_note(
        user=user_no_access,
        applicant=new_job_posting_applicant,
    )
    assert can_user_view == False


###################################
# APPLICANT NOTE CREATE PERMISSIONS
###################################
def test_add_all_applicant_notes(user_no_access):
    user_service.add_user_group(
        user_id=user_no_access.id,
        group_name=permission_constants.Groups.applicant_note_add_all,
    )
    assert applicant_rules.can_add_all_applicant_notes(user_no_access) == True


def test_add_job_posting_applicant_notes(user_no_access, applicant):
    permission_utils.create_user_job_posting_applicant_note_permission(
        user_id=user_no_access.id,
        job_posting_id=applicant.job_posting.id,
        permission_codename=permission_constants.ObjectPermissions.applicant_note_add,
    )
    can_user_add = applicant_rules.can_add_job_posting_applicant_notes(
        user=user_no_access, applicant=applicant
    )
    assert can_user_add == True

    second_applicant = factories.ApplicantFactory(
        job_posting_id=applicant.job_posting_id
    )
    can_user_add = applicant_rules.can_add_job_posting_applicant_notes(
        user=user_no_access,
        applicant=second_applicant,
    )
    assert can_user_add == True

    new_job_posting_applicant = factories.ApplicantFactory()
    can_user_add = applicant_rules.can_add_job_posting_applicant_notes(
        user=user_no_access,
        applicant=new_job_posting_applicant,
    )
    assert can_user_add == False


def test_add_applicant_note(user_no_access, applicant):
    permission_utils.create_user_applicant_note_permission(
        user_id=user_no_access.id,
        applicant_id=applicant.id,
        permission_codename=permission_constants.ObjectPermissions.applicant_note_add,
    )
    can_user_add = applicant_rules.can_add_applicant_note(
        user=user_no_access,
        applicant=applicant,
    )
    assert can_user_add == True

    second_applicant = factories.ApplicantFactory(
        job_posting_id=applicant.job_posting_id
    )
    can_user_add = applicant_rules.can_add_applicant_note(
        user=user_no_access,
        applicant=second_applicant,
    )
    assert can_user_add == False

    new_job_posting_applicant = factories.ApplicantFactory()
    can_user_add = applicant_rules.can_add_applicant_note(
        user=user_no_access,
        applicant=new_job_posting_applicant,
    )
    assert can_user_add == False
