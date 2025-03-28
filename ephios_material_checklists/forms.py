from django.forms import modelformset_factory, BooleanField, BaseModelFormSet
from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.translation import gettext as _

from ephios_material_checklists.models import ItemTypeCategory, ItemType


class BaseItemTypeFormset(BaseModelFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        initial_form_count = self.initial_form_count()
        if self.can_delete and (self.can_delete_extra or index < initial_form_count):
            itemtype: ItemType = form.instance
            form.fields[DELETION_FIELD_NAME] = BooleanField(
                label=_("Delete"),
                required=False,
                disabled=itemtype.pk and itemtype.checklistentry_set.exists(),
            )


ItemTypeFormset = modelformset_factory(
    ItemType,
    formset=BaseItemTypeFormset,
    can_delete=True,
    extra=0,
    fields=["name", "notes", "has_expiry_date", "deprecated"],
)

