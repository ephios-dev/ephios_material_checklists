import os.path

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from easy_thumbnails.fields import ThumbnailerImageField


from .itemtype import ItemType


def checklist_file_path(instance, filename):
    return "checklist/{0}/pdf/{1}".format(instance.pk, filename)


def checklist_image_path(instance, filename):
    path_without_extension, file_extension = os.path.splitext(filename)
    return "checklist/{0}/image/checklist{1}{2}".format(
        instance.pk, instance.pk, file_extension
    )


def checklist_compartment_image_path(instance, filename):
    path_without_extension, file_extension = os.path.splitext(filename)
    return "checklist/{0}/image/compartment{1}{2}".format(
        instance.checklist().pk, instance.pk, file_extension
    )


class Checklist(models.Model):
    name = models.CharField(max_length=254, unique=True, verbose_name=_("name"))
    # TODO: Add field for reference list of fulfilled specifications to allow quick access.
    # fulfilled_specification_lists = models.ManyToManyField(MaterialSpecificationList,
    #                                                        related_name="implementing_checklists")
    deprecated = models.BooleanField(default=False, verbose_name=_("deprecated"))
    abstract = models.BooleanField(default=False, verbose_name=_("only sub-checklist"))

    file = models.FileField(
        upload_to=checklist_file_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        verbose_name=_("pdf file"),
    )

    image = ThumbnailerImageField(
        upload_to=checklist_image_path, blank=True, verbose_name=_("image")
    )

    def save(self, *args, **kwargs):
        self.parent = None
        return super(Checklist, self).save(*args, **kwargs)

    def get_parent_checklists(self, ignore_compartments=None):
        if ignore_compartments is None:
            ignore_compartments = []
        collected_parents = []
        for parent in ChecklistCompartmentWithExternalChecklist.objects.filter(
            external_checklist=self
        ).all():
            if parent not in ignore_compartments:
                collected_parents.append(parent.checklist())
                collected_parents += parent.checklist().get_parent_checklists()
        return collected_parents

    def get_child_checklists(self, ignore_compartments=None):
        if ignore_compartments is None:
            ignore_compartments = []
        collected_children = []
        for child in [
            compartment.external_checklist
            for compartment in self.get_all_compartments()
            if compartment.has_external_checklist()
            and compartment not in ignore_compartments
        ]:
            collected_children.append(child)
            # collected_children += child.get_child_checklists()
        return collected_children

    def get_related_checklists(self, ignore_compartments=None):
        return (
            self.get_parent_checklists(ignore_compartments)
            + self.get_child_checklists(ignore_compartments)
            + [self]
        )

    def get_compartments(self):
        compartment_list = []
        for compartment in self.compartments.order_by("name"):
            if compartment.has_external_checklist():
                compartment_list.append(
                    compartment.checklistcompartmentwithexternalchecklist
                )
            else:
                compartment_list.append(compartment)
        return compartment_list

    def get_all_compartments(self):
        compartment_list = []
        for compartment in self.get_compartments():
            compartment_list.append(compartment)
            compartment_list.extend(compartment.get_all_compartments())
        return compartment_list

    def get_all_entries(self):
        entries = ChecklistEntry.objects.none()
        for compartment in self.get_compartments():
            entries = entries.union(compartment.get_all_entries())
        return entries

    def get_entry_count(self):
        return len(self.get_all_entries())

    def get_item_count(self):
        return sum([entry.amount for entry in self.get_all_entries()])

    def get_ordered_entries(self):
        entries = [e for e in self.get_all_entries()]
        entries.sort(key=lambda x: x.amount)
        entries.sort(key=lambda x: x.item_type.name)
        entries.sort(key=lambda x: x.item_type.category.name)
        entries.sort(key=lambda x: x.item_type.category.order_key)
        return entries

    def get_merged_entries(self):
        merged_entries = []
        prev_entry = None
        for entry in self.get_ordered_entries():
            if prev_entry and entry.item_type == prev_entry.item_type:
                prev_entry.amount += entry.amount
                prev_entry.compartment = (
                    None  # Set compartment to null to prevent accidental save().
                )
            else:
                merged_entries.append(entry)
                prev_entry = entry
        return merged_entries

    def get_merged_entry_count(self):
        return len(self.get_merged_entries())

    def copy_compartments_from(self, other_checklist):
        # Check that target checklist (i.e. self) is empty
        if self.get_compartments():
            return  # Should only work if no contents exist yet

        # Copy sub-compartments
        for other_sub_compartment in other_checklist.get_compartments():
            if other_sub_compartment.has_external_checklist():
                ChecklistCompartmentWithExternalChecklist.objects.create(
                    name=other_sub_compartment.name,
                    parent_checklist=self,
                    external_checklist=other_sub_compartment.external_checklist,
                )
            else:
                new_sub_compartment = ChecklistCompartment.objects.create(
                    name=other_sub_compartment.name, parent_checklist=self
                )
                new_sub_compartment.copy_content_from(other_sub_compartment)

    def get_absolute_url(self):
        return reverse("material:checklist_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("checklist")
        verbose_name_plural = _("checklists")


class ChecklistCompartment(models.Model):
    name = models.CharField(max_length=254, verbose_name=_("name"))
    parent_compartment = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="sub_compartments",
        verbose_name=_("parent compartment"),
    )
    parent_checklist = models.ForeignKey(
        Checklist,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="compartments",
        verbose_name=_("parent checklist"),
    )

    image = ThumbnailerImageField(
        upload_to=checklist_compartment_image_path,
        blank=True,
        verbose_name=_("image"),
    )

    def __init__(self, *args, **kwargs):
        self.available_itemtypes_queryset = None
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Ensure existence of ONE parent object
        if self.parent_compartment and self.parent_checklist:
            raise ValidationError(
                "A compartment cannot be at top level of a checklist "
                + "AND inside another compartment at the same time."
            )
        if not self.parent_compartment and not self.parent_checklist:
            raise ValidationError(
                "A compartment must be at top level of a checklist OR inside another compartment."
            )

        # Loop prevention 1: Ensure parent compartment is not self or having checklist
        if self.parent_compartment:
            if self.parent_compartment == self:
                raise ValidationError("A compartment cannot be inside itself.")
            if (
                type(self.parent_compartment)
                is ChecklistCompartmentWithExternalChecklist
            ):
                raise ValidationError(
                    "A compartment cannot be inside a compartment that has its own checklist."
                )

        # Loop prevention 2: Ensure parent compartment is part of own sub-compartments
        # (Skip this step if instance is newly created, since it cannot have sub-compartments by then already)
        if self.id is not None:
            if self.parent_compartment in self.get_all_compartments():
                raise ValidationError(
                    "A compartment cannot be inside it's own sub compartment."
                )

        return super().save(*args, **kwargs)

    def get_sub_compartments(self):
        compartment_list = []
        for compartment in self.sub_compartments.order_by("name"):
            if compartment.has_external_checklist():
                compartment_list.append(
                    compartment.checklistcompartmentwithexternalchecklist
                )
            else:
                compartment_list.append(compartment)
        return compartment_list

    def get_all_compartments(self):
        compartment_list = []
        for sub_compartment in self.get_sub_compartments():
            compartment_list.append(sub_compartment)
            compartment_list.extend(sub_compartment.get_all_compartments())
        return compartment_list

    def has_external_checklist(self):
        return hasattr(self, "checklistcompartmentwithexternalchecklist")

    def get_local_entries(self):
        return self.contents.all().prefetch_related("item_type", "item_type__category")

    def get_ordered_local_entries(self):
        return (
            self.get_local_entries()
            .order_by(
                "item_type__category__order_key",
                "item_type__category__name",
                "item_type__name",
            )
            .distinct()
        )

    def get_all_entries(self):
        entries = self.get_local_entries()
        for sub_compartment in self.get_sub_compartments():
            entries = entries.union(sub_compartment.get_all_entries())
        return entries

    def checklist(self):
        if self.parent_checklist:
            return self.parent_checklist
        if self.parent_compartment:
            return self.parent_compartment.checklist()
        return None

    def get_available_itemtypes(self):
        if not self.available_itemtypes_queryset:
            merged_queryset = ItemType.objects.filter(
                checklistentry__compartment=self
            ) | ItemType.objects.filter(deprecated=False)
            self.available_itemtypes_queryset = merged_queryset.order_by(
                "category__order_key", "categoryp__name", "name"
            ).distinct()
        return self.available_itemtypes_queryset

    def copy_content_from(self, other_compartment):
        # Check that target compartment (i.e. self) is empty
        if self.get_local_entries() or self.get_sub_compartments():
            return  # Should only work if no contents exist yet

        # Copy contained entries
        for other_entry in other_compartment.get_local_entries():
            ChecklistEntry.objects.create(
                item_type=other_entry.item_type,
                compartment=self,
                amount=other_entry.amount,
                optional=other_entry.optional,
                notes=other_entry.notes,
            )

        # Copy sub-compartments
        for other_sub_compartment in other_compartment.get_sub_compartments():
            if other_sub_compartment.has_external_checklist():
                ChecklistCompartmentWithExternalChecklist.objects.create(
                    name=other_sub_compartment.name,
                    parent_compartment=self,
                    external_checklist=other_sub_compartment.external_checklist,
                )
            else:
                new_sub_compartment = ChecklistCompartment.objects.create(
                    name=other_sub_compartment.name, parent_compartment=self
                )
                new_sub_compartment.copy_content_from(other_sub_compartment)

    def __str__(self):
        if self.parent_checklist:
            return str(self.parent_checklist) + " : " + self.name
        return str(self.parent_compartment) + " : " + self.name

    class Meta:
        verbose_name = _("checklist compartment")
        verbose_name_plural = _("checklist compartments")
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "parent_checklist"],
                condition=models.Q(parent_compartment__isnull=True),
                name="name_is_unique_in_checklist",
            ),
            models.UniqueConstraint(
                fields=["name", "parent_compartment"],
                condition=models.Q(parent_checklist__isnull=True),
                name="name_is_unique_in_compartment",
            ),
        ]


class ChecklistCompartmentWithExternalChecklist(ChecklistCompartment):
    external_checklist = models.ForeignKey(
        Checklist,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name=_("referenced checklist"),
    )

    def get_all_entries(self):
        return self.external_checklist.get_all_entries()

    def save(self, *args, **kwargs):
        # Ensure that no checklist references itself
        if self.checklist() == self.external_checklist:
            raise ValidationError(
                "A compartment cannot reference the checklist that contains it."
            )

        # Ensure that no checklist is referenced twice (also not by parent or sub checklists)
        related_checklists = self.checklist().get_related_checklists(
            ignore_compartments=[self]
        )
        for checklist in [
            self.external_checklist
        ] + self.external_checklist.get_child_checklists():
            if any(
                [
                    compartment.checklist() in related_checklists
                    for compartment in ChecklistCompartmentWithExternalChecklist.objects.filter(
                        external_checklist=checklist
                    ).all()
                    if compartment != self
                ]
            ):
                raise ValidationError(
                    "Checklist "
                    + str(checklist)
                    + " should only be referenced once from "
                    + str(self.checklist())
                    + " or any related checklist."
                )

        # Ensure that there are no cyclic checklist references
        if any(
            [
                compartment.external_checklist == self.checklist()
                for compartment in self.external_checklist.get_all_compartments()
                if compartment.has_external_checklist()
            ]
        ):
            raise ValidationError(
                "Referenced external checklist should not contain link to self."
            )

        # Save the object
        return super(ChecklistCompartmentWithExternalChecklist, self).save(
            *args, **kwargs
        )

    def get_sub_compartments(self):
        return self.external_checklist.get_compartments()

    def __str__(self):
        return _("{compartment} (contents according to checklist {checklist})").format(
            compartment=super().__str__(),
            checklist=self.external_checklist.name,
        )

    class Meta:
        verbose_name = _("checklist compartment containing other checklist")
        verbose_name_plural = _("checklist compartments containing other checklists")


class ChecklistEntry(models.Model):
    item_type = models.ForeignKey(
        ItemType, blank=False, null=False, on_delete=models.CASCADE, verbose_name="item type",
    )
    compartment = models.ForeignKey(
        ChecklistCompartment,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="contents",
        verbose_name=_("compartment"),
    )
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="required amount")
    optional = models.BooleanField(default=False, verbose_name="optional")
    notes = models.TextField(blank=True, verbose_name=_("notes"))

    def print_amount(self):
        if self.optional:
            return "[ " + str(self.amount) + " ]"
        else:
            return str(self.amount)

    def checklist(self):
        return self.compartment.checklist()

    def save(self, *args, **kwargs):
        if self.compartment and self.compartment.has_external_checklist():
            raise ValidationError(
                "Entries cannot be inside compartments that bring their own checklist."
            )
        return super(ChecklistEntry, self).save(*args, **kwargs)

    def __str__(self):
        return (
            str(self.amount)
            + "x "
            + str(self.item_type)
            + " in "
            + str(self.compartment)
        )

    def __hash__(self):
        return hash(self.pk + self.amount + self.item_type.pk)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.pk == other.pk
            and self.item_type == other.item_type
            and self.amount == other.amount
        )

    class Meta:
        verbose_name = _("checklist entry")
        verbose_name_plural = _("checklist entries")
        unique_together = [["compartment", "item_type"]]
