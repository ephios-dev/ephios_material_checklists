from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

from ephios_material_checklists.models import Checklist


class ChecklistListView(ListView):
    model = Checklist
    template_name = "ephios_material_checklists/checklist_list.html"


class ChecklistCreateView(SuccessMessageMixin, CreateView):
    model = Checklist
    fields = ("name", "abstract", "image")
    success_message = _("Checklist %(name)s was created successfully. You can now specify it's contents.")

    def get_success_url(self):
        return reverse("ephios_material_checklists:checklist_detail", kwargs={"pk": self.object.pk})


class ChecklistDetailView(DetailView):
    model = Checklist
    context_object_name = 'this_checklist'
    template_name = "ephios_material_checklists/checklist_detail.html"


class ChecklistUpdateView(SuccessMessageMixin, UpdateView):
    model = Checklist
    fields = ("name", "abstract", "deprecated", "image")
    success_message = _("Checklist %(name)s was updated successfully.")

    def get_success_url(self):
        return reverse("ephios_material_checklists:checklist_edit_start", kwargs={"pk": self.object.pk})


class ChecklistUpdatePDFView(ChecklistUpdateView):
    fields = ("file",)

    def get_success_message(self, cleaned_data):
        if self.object.file:
            return _("Referenced PDF for %(name)s was set successfully.") % dict(name=self.object.name, )
        else:
            return _("Referenced PDF for %(name)s was removed successfully.") % dict(name=self.object.name, )


class ChecklistDeleteView(SuccessMessageMixin, DeleteView):
    model = Checklist
    success_url = reverse_lazy("ephios_material_checklists:checklist_list")
    success_message = _("Checklist %(name)s was deleted successfully.")

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(name=self.object.name, )


class ChecklistDetailContentView(ChecklistDetailView):
    template_name = "ephios_material_checklists/checklist_content.html"


class ChecklistEditStartView(
    # ChecklistHierarchyMixin,
    ChecklistDetailView
):
    template_name = "ephios_material_checklists/checklist_edit_start.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['hierarchical_compartment_list'] = self.checklist_to_indented_list(context['this_checklist'],
    #                                                                                start_level=0, include_entries=False,
    #                                                                                include_external_content=False)
    #     return context

# class ChecklistDetailHierarchyView(ChecklistHierarchyMixin, ChecklistDetailView):
#     template_name = "material/checklist/detail_hierarchy.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['hierarchical_list'] = self.checklist_to_indented_list(context['this_checklist'])
#         return context
