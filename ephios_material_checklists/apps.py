from ephios.core.plugins import PluginConfig


class PluginApp(PluginConfig):
    name = "ephios_material_checklists"

    class EphiosPluginMeta:
        name = "ephios_material_checklists"
        author = "Christian Schäffer <dev@cschaeffer.de>"
        description = "Create and manage checklists to keep track of consumable material"

    def ready(self):
        from . import signals  # NOQA
