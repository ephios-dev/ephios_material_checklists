from django.urls import path, include

from .views import ChecklistsStartView
from .views.checklist import ChecklistListView

app_name = "ephios_material_checklists"

urlpatterns = [
    path(
        "checklists/",
        include(
            [
                path("", ChecklistListView.as_view(), name="checklist_list"),
            ],
            "",
        ),
    ),
]
