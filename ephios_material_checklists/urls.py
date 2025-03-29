from django.urls import path, include

from .views import ChecklistListView, ChecklistDetailView, ItemTypeCategoryListView, ItemTypeCategoryUpdateView, \
    ItemTypeCategoryCreateView, ItemTypeSetUpdateView, ChecklistDetailContentView

app_name = "ephios_material_checklists"

urlpatterns = [
    path(
        "checklists/",
        include(
            [
                path("", ChecklistListView.as_view(), name="checklist_list"),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path("", ChecklistDetailView.as_view(), name="checklist_detail"),
                            path("content/", ChecklistDetailContentView.as_view(), name="checklist_content"),
                        ],
                        "",
                    ),
                ),
                path(
                    "itemtypes/",
                    include(
                        [
                            path("", ItemTypeCategoryListView.as_view(), name="itemtype_category_list"),
                            path("add/", ItemTypeCategoryCreateView.as_view(), name="itemtype_category_add"),
                            path("<int:category_pk>/", ItemTypeSetUpdateView.as_view(), name="itemtype_edit"),
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
