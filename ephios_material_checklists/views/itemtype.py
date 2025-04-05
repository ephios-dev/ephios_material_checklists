from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, FormView, DeleteView

from ephios_material_checklists.forms import ItemTypeFormset
from ephios_material_checklists.models import ItemTypeCategory


class ChecklistsStartView(TemplateView):
    template_name = "ephios_material_checklists/start.html"

class ItemTypeCategoryListView(ListView):
    model = ItemTypeCategory
    ordering = ("order_key", "name")

    def get_queryset(self):
        return super().get_queryset().prefetch_related("items")

class ItemTypeCategoryCreateView(SuccessMessageMixin, CreateView):
    model = ItemTypeCategory
    fields = ("name", "order_key")
    success_message = _("Category %(name)s was created successfully. You can now specify the material types.")

    def get_success_url(self):
        return reverse("ephios_material_checklists:itemtype_edit",  kwargs={"pk": self.object.pk})

class ItemTypeCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = ItemTypeCategory
    fields = ("name", "order_key")
    success_url = reverse_lazy("ephios_material_checklists:itemtype_category_list")
    success_message = _("Material type category %(name)s was update successfully.")

class ItemTypeCategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = ItemTypeCategory
    success_url = reverse_lazy("ephios_material_checklists:itemtype_category_list")
    success_message = _("Category %(name)s and it's material types were deleted successfully.")

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(name=self.object.name, )

class ItemTypeSetUpdateView(SuccessMessageMixin, FormView):
    form_class = ItemTypeFormset
    template_name = "ephios_material_checklists/itemtype_set_form.html"
    success_message = _("Material types were updated successfully.")

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(ItemTypeCategory, pk=self.kwargs.pop("pk"))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        # return {"category": self.category, **super().get_form_kwargs()}
        return {"instance": self.category, **super().get_form_kwargs()}

    def get_context_data(self, **kwargs):
        return {"category": self.category, **super().get_context_data(**kwargs)}

    def get_success_url(self):
        return reverse("ephios_material_checklists:itemtype_edit",  kwargs={"pk": self.category.pk})

    def form_valid(self, form):
        # form.category = self.category
        with transaction.atomic():
            form.save()
        return super().form_valid(form)

