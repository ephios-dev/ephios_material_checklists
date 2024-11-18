from django.contrib import admin

from ephios_material_checklists.models import Checklist, ItemType, ItemTypeCategory

admin.site.register(Checklist)
admin.site.register(ItemType)
admin.site.register(ItemTypeCategory)