from django.urls import path, include

from .views import ChecklistListView, ChecklistDetailView, ItemtypeListView

app_name = "ephios_material_checklists"

urlpatterns = [
    path(
        "checklists/",
        include(
            [
                path("", ChecklistListView.as_view(), name="checklist_list"),
                path("<int:pk>/", ChecklistDetailView.as_view(), name="checklist_detail"),
                path(
                    "itemtypes/",
                    include(
                        [
                            path("", ItemtypeListView.as_view(), name="itemtype_list"),
                        ],
                        "",
                    ),
                ),
            ],
            "",
        ),
    ),
]
