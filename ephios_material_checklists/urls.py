from django.urls import path, include

from .views import ChecklistListView, ChecklistDetailView, ItemTypeCategoryListView, ItemTypeCategoryUpdateView, \
    ItemTypeCategoryCreateView, ItemTypeSetUpdateView, ChecklistDetailContentView, ChecklistCreateView, \
    ChecklistUpdateView, ItemTypeCategoryDeleteView, ChecklistEditStartView, ChecklistUpdatePDFView, ChecklistDeleteView

app_name = "ephios_material_checklists"

urlpatterns = [
    path(
        "checklists/",
        include(
            [
                path("", ChecklistListView.as_view(), name="checklist_list"),
                path("add/", ChecklistCreateView.as_view(), name="checklist_add"),
                path(
                    "<int:pk>/",
                    include(
                        [
                            path("", ChecklistDetailView.as_view(), name="checklist_detail"),
                            path("content/", ChecklistDetailContentView.as_view(), name="checklist_content"),
                            path("delete/", ChecklistDeleteView.as_view(), name="checklist_delete"),
                            path("edit/",
                                include(
                                    [
                                        path("", ChecklistEditStartView.as_view(), name="checklist_edit_start"),
                                        path("details/", ChecklistUpdateView.as_view(), name="checklist_edit_details"),
                                        path("pdf/", ChecklistUpdatePDFView.as_view(), name="checklist_edit_pdf"),
                                    ],
                                    "",
                                ),
                            ),
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
                            path(
                                "<int:pk>/",
                                include(
                                    [
                                        path("", ItemTypeSetUpdateView.as_view(), name="itemtype_edit"),
                                        path("edit/", ItemTypeCategoryUpdateView.as_view(), name="itemtype_category_edit"),
                                        path("delete/", ItemTypeCategoryDeleteView.as_view(), name="itemtype_category_delete"),
                                    ],
                                    "",
                                ),
                            ),
                        ],
                        "",
                    ),
                ),
            ],
            "",
        ),
    ),
]
