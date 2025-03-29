from django.db.models import ForeignKey
from django.forms import BooleanField, BaseModelFormSet, inlineformset_factory, modelformset_factory, ModelForm, \
    BaseInlineFormSet
from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.translation import gettext as _

from ephios_material_checklists.models import ItemType, ItemTypeCategory


class BaseItemTypeFormset(BaseInlineFormSet):

    #def __init__(self, *args, **kwargs):
    #    self.category = kwargs.pop("category")
    #    super().__init__(*args, **kwargs)
    #    self.queryset = ItemType.objects.filter(category=self.category).order_by("name")

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

    # def clean(self):
    #     super().clean()
    #
    #     for form in self.forms:
    #         form.instance.category = self.category
    #         print(form.cleaned_data, form.instance.category)


ItemTypeFormset = inlineformset_factory(
    model=ItemType,
    parent_model=ItemTypeCategory,
    formset=BaseItemTypeFormset,
    can_delete=True,
    can_order=False,
    extra=0,
    fields=["name", "notes", "has_expiry_date", "deprecated"],
)

