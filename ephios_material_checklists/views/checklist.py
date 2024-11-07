from django.views.generic import ListView, DetailView

from ephios_material_checklists.models import Checklist


class ChecklistListView(ListView):
    model = Checklist
    template_name = "ephios_material_checklists/checklist/checklist_list.html"


class ChecklistDetailView(DetailView):
    model = Checklist
    context_object_name = 'this_checklist'
    template_name = "ephios_material_checklists/checklist/detail.html"


class ChecklistDetailContentView(ChecklistDetailView):
    template_name = "ephios_material_checklists/checklist/detail_content.html"


# class ChecklistDetailHierarchyView(ChecklistHierarchyMixin, ChecklistDetailView):
#     template_name = "material/checklist/detail_hierarchy.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['hierarchical_list'] = self.checklist_to_indented_list(context['this_checklist'])
#         return context