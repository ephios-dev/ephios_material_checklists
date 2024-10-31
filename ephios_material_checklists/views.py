from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from ephios.extra.mixins import CustomPermissionRequiredMixin
from ephios.plugins.simpleresource.models import Resource


# Create your views here.
class ChecklistsStartView(CustomPermissionRequiredMixin, TemplateView):
    permission_required = "ephios_material_checklists.add_checklist"
    template_name = "ephios_material_checklists/start.html"

# class ChecklistsStartView(CustomPermissionRequiredMixin, ListView):
#     permission_required = "simpleresource.view_resourcecategory"
#     model = Resource
#     ordering = ("category__name", "title")
#
#     def get_queryset(self):
#         return super().get_queryset().select_related("category")