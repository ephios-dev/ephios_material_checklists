from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from ephios.extra.mixins import CustomPermissionRequiredMixin
from ephios.plugins.simpleresource.models import Resource

from ephios_material_checklists.models import ItemType


class ChecklistsStartView(TemplateView):
    template_name = "ephios_material_checklists/start.html"

class ItemtypeListView(ListView):
    model = ItemType
    ordering = ("category__order_key", "category__name", "name")
    template_name = "ephios_material_checklists/itemtype/itemtype_list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("category")