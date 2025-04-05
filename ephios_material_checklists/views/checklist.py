from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from ephios_material_checklists.models import Checklist


class ChecklistListView(ListView):
    model = Checklist
    template_name = "ephios_material_checklists/checklist_list.html"

class ChecklistCreateView(CreateView):
    model = Checklist
    fields = ("name", "abstract", "image")

    def get_success_url(self):
        return reverse("ephios_material_checklists:checklist_detail",  kwargs={"pk": self.object.pk})

class ChecklistDetailView(DetailView):
    model = Checklist
    context_object_name = 'this_checklist'
    template_name = "ephios_material_checklists/checklist_detail.html"

class ChecklistUpdateView(UpdateView):
    model = Checklist
    fields = ("name", "abstract", "image")

    def get_success_url(self):
        return reverse("ephios_material_checklists:checklist_edit_start",  kwargs={"pk": self.object.pk})

class ChecklistUpdatePDFView(ChecklistUpdateView):
    fields = ("file", )

class ChecklistDeleteView(DeleteView):
    model = Checklist
    success_url = reverse_lazy("ephios_material_checklists:checklist_list")

class ChecklistDetailContentView(ChecklistDetailView):
    template_name = "ephios_material_checklists/checklist_content.html"


class ChecklistEditStartView(
    #ChecklistHierarchyMixin,
    ChecklistDetailView
):
    template_name = "ephios_material_checklists/checklist_edit_Start.html"

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