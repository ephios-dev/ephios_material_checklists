from ephios.core.plugins import PluginConfig
from django.utils.translation import gettext_lazy as _


class PluginApp(PluginConfig):
    name = "ephios_material_checklists"

    class EphiosPluginMeta:
        name = _("Material Checklists")
        author = "Christian Schäffer <dev@cschaeffer.de>"
        description = _(
            "Create and manage checklists to keep track of consumable material."
        )

    def ready(self):
        from . import signals  # NOQA
