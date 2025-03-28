from django.contrib import admin

from ephios_material_checklists.models import Checklist, ItemType, ItemTypeCategory, ChecklistCompartment, \
    ChecklistCompartmentWithExternalChecklist, ChecklistEntry

admin.site.register(Checklist)
admin.site.register(ChecklistCompartment)
admin.site.register(ChecklistCompartmentWithExternalChecklist)
admin.site.register(ChecklistEntry)

admin.site.register(ItemType)
admin.site.register(ItemTypeCategory)