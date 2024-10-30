from ephios.core.plugins import PluginConfig


class PluginApp(PluginConfig):
    name = "ephios_material_checklists"

    class EphiosPluginMeta:
        name = "ephios_material_checklists"
        author = "Julian Baumann <julian@ephios.de>"
        description = "Manage material and create checklists to keep track of it"

    def ready(self):
        from . import signals  # NOQA
