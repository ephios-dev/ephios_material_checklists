from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from ephios.extra.mixins import CustomPermissionRequiredMixin
from ephios.plugins.simpleresource.models import Resource

from ephios_material_checklists.models import ItemType, ItemTypeCategory


class ChecklistsStartView(TemplateView):
    template_name = "ephios_material_checklists/start.html"

class ItemTypeCategoryListView(ListView):
    model = ItemTypeCategory
    ordering = ("order_key", "name")

    def get_queryset(self):
        return super().get_queryset().prefetch_related("items")

class ItemTypeCategoryCreateView(CreateView):
    model = ItemTypeCategory
    fields = ("name", "order_key")

    def get_success_url(self):
        return reverse("ephios_material_checklists:itemtype_category_edit",  kwargs={"pk": self.object.pk})

class ItemTypeCategoryUpdateView(UpdateView):
    model = ItemTypeCategory
    fields = ("name", "order_key")
    success_url = reverse_lazy("ephios_material_checklists:itemtype_category_list")