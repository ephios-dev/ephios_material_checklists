from django.urls import path, include

from .views import ChecklistListView, ChecklistDetailView, ItemTypeCategoryListView, ItemTypeCategoryUpdateView

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
                            path("", ItemTypeCategoryListView.as_view(), name="itemtype_category_list"),
                            path("<int:pk>/edit/", ItemTypeCategoryUpdateView.as_view(), name="itemtype_category_edit"),
                        ],
                        "",
                    ),
                ),
            ],
            "",
        ),
    ),
]
