from django.urls import path

from .views import ChecklistsStartView

app_name = "ephios_material_checklists"

urlpatterns = [
    path("checklists/", ChecklistsStartView.as_view(), name="start"),
]