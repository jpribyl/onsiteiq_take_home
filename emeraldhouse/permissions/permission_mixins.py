from rules.contrib import rest_framework as rules_rest_framework


class CustomAutoPermissionViewSetMixin(rules_rest_framework.AutoPermissionViewSetMixin):
    """
    Enforces object-level permissions in ``rest_framework.viewsets.ViewSet``,
    deriving the permission type from the particular action to be performed..

    As with ``rules.contrib.views.AutoPermissionRequiredMixin``, this only works when
    model permissions are registered using ``rules.contrib.models.RulesModelMixin``.
    """

    # Maps API actions to model permission types. None as value skips permission
    # checks for the particular action.
    # This map needs to be extended when custom actions are implemented
    # using the @action decorator.
    # Extend or replace it in subclasses like so:
    # permission_type_map = {
    #     **AutoPermissionViewSetMixin.permission_type_map,
    #     "close": "change",
    #     "reopen": "change",
    # }
    permission_type_map = {
        **rules_rest_framework.AutoPermissionViewSetMixin.permission_type_map,
        "list": "list",
        "transition_applicant": "change",
        "add_note": "add_note",
        "view_notes": "view_notes",
    }
