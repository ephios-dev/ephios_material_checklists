from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from ephios.core.signals import (
    nav_link, register_group_permission_fields,
)
from ephios.extra.permissions import PermissionField


# Register to ephios signals here


@receiver(nav_link, dispatch_uid="ephios_material_checklists.signals.add_nav_link")
def add_nav_link(sender, request, **kwargs):
    return (
        [
            {
                "label": _("Checklists"),
                "url": reverse_lazy("ephios_material_checklists:start"),
                "active": request.resolver_match
                and request.resolver_match.app_name == "ephios_material_checklists",
                "group": _("Management"),
            }
        ]
        if request.user.has_perm("ephios_material_checklists.add_checklist")
        else []
    )

@receiver(
    register_group_permission_fields,
    dispatch_uid="ephios_material_checklists.signals.checklist_group_permission_fields",
)
def checklist_group_permission_fields(sender, **kwargs):
    return [
        (
            "manage_checklists",
            PermissionField(
                label=_("Manage checklists"),
                help_text=_("Allows to create, edit and delete checklists."),
                permissions=[
                    "ephios_material_checklists.add_checklist",
                    "ephios_material_checklists.update_checklist",
                    "ephios_material_checklists.delete_checklist",
                ],
            ),
        )
    ]