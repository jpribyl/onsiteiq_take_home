class AppLabels:
    emeraldhouse: str = "emeraldhouse"


class ModelNames:
    applicant = "applicant"
    applicant_note = "applicantnote"
    job_posting = "jobposting"


class Actions:
    view = "view"
    view_all = "view_all"
    add = "add"
    add_all = "add_all"
    change = "change"
    change_all = "change_all"
    delete = "delete"
    delete_all = "delete_all"


class ObjectPermissions:
    applicant_add = f"{Actions.add}_{ModelNames.applicant}"
    applicant_view = f"{Actions.view}_{ModelNames.applicant}"
    applicant_change = f"{Actions.change}_{ModelNames.applicant}"

    applicant_note_add = f"{Actions.add}_{ModelNames.applicant_note}"
    applicant_note_view = f"{Actions.view}_{ModelNames.applicant_note}"


class Groups:
    applicant_view_all = f"{Actions.view_all}_{ModelNames.applicant}"
    applicant_add_all = f"{Actions.add_all}_{ModelNames.applicant}"
    applicant_change_all = f"{Actions.change_all}_{ModelNames.applicant}"

    applicant_note_view_all = f"{Actions.view_all}_{ModelNames.applicant_note}"
    applicant_note_add_all = f"{Actions.add_all}_{ModelNames.applicant_note}"
