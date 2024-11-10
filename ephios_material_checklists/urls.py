from django.urls import path, include

from .views import ChecklistsStartView, ChecklistDetailView
from .views.checklist import ChecklistListView

app_name = "ephios_material_checklists"

urlpatterns = [
    path(
        "checklists/",
        include(
            [
                path("", ChecklistListView.as_view(), name="checklist_list"),
                path("<int:pk>/", ChecklistDetailView.as_view(), name="checklist_detail"),
            ],
            "",
        ),
    ),
]
