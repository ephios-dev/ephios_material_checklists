from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView
from ephios.extra.mixins import CustomPermissionRequiredMixin
from ephios.plugins.simpleresource.models import Resource

from ephios_material_checklists.models import ItemType, ItemTypeCategory


class ChecklistsStartView(TemplateView):
    template_name = "ephios_material_checklists/start.html"

class ItemTypeCategoryListView(ListView):
    model = ItemTypeCategory
    ordering = ("order_key", "name")
    template_name = "ephios_material_checklists/itemtype/itemtypecategory_list.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("items")

class ItemTypeCategoryUpdateView(UpdateView):
    model = ItemTypeCategory
    # fields = ("title", "category")
    success_url = reverse_lazy("ephios_material_checklists:itemtype_category_edit")