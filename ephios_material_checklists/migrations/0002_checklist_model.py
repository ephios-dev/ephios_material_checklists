# Generated by Django 5.1.3 on 2024-11-07 00:27

import django.core.validators
import django.db.models.deletion
import easy_thumbnails.fields
import ephios_material_checklists.models.checklist
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ephios_material_checklists", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Checklist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=254, unique=True, verbose_name="Name"),
                ),
                (
                    "deprecated",
                    models.BooleanField(default=False, verbose_name="deprecated"),
                ),
                (
                    "abstract",
                    models.BooleanField(
                        default=False, verbose_name="only sub-checklist"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=ephios_material_checklists.models.checklist.checklist_file_path,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf"]
                            )
                        ],
                        verbose_name="pdf file",
                    ),
                ),
                (
                    "image",
                    easy_thumbnails.fields.ThumbnailerImageField(
                        blank=True,
                        upload_to=ephios_material_checklists.models.checklist.checklist_image_path,
                        verbose_name="image",
                    ),
                ),
            ],
            options={
                "verbose_name": "checklist",
                "verbose_name_plural": "checklists",
            },
        ),
        migrations.CreateModel(
            name="ChecklistCompartment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=254, verbose_name="Name")),
                (
                    "image",
                    easy_thumbnails.fields.ThumbnailerImageField(
                        blank=True,
                        upload_to=ephios_material_checklists.models.checklist.checklist_compartment_image_path,
                        verbose_name="image",
                    ),
                ),
                (
                    "parent_checklist",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="compartments",
                        to="ephios_material_checklists.checklist",
                        verbose_name="parent checklist",
                    ),
                ),
                (
                    "parent_compartment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_compartments",
                        to="ephios_material_checklists.checklistcompartment",
                        verbose_name="parent compartment",
                    ),
                ),
            ],
            options={
                "verbose_name": "checklist compartment",
                "verbose_name_plural": "checklist compartments",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ChecklistEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="required amount",
                    ),
                ),
                (
                    "optional",
                    models.BooleanField(default=False, verbose_name="optional"),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "compartment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contents",
                        to="ephios_material_checklists.checklistcompartment",
                        verbose_name="compartment",
                    ),
                ),
                (
                    "item_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ephios_material_checklists.itemtype",
                        verbose_name="item type",
                    ),
                ),
            ],
            options={
                "verbose_name": "checklist entry",
                "verbose_name_plural": "checklist entries",
            },
        ),
        migrations.CreateModel(
            name="ChecklistCompartmentWithExternalChecklist",
            fields=[
                (
                    "checklistcompartment_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="ephios_material_checklists.checklistcompartment",
                    ),
                ),
                (
                    "external_checklist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ephios_material_checklists.checklist",
                        verbose_name="referenced checklist",
                    ),
                ),
            ],
            options={
                "verbose_name": "checklist compartment containing other checklist",
                "verbose_name_plural": "checklist compartments containing other checklists",
            },
            bases=("ephios_material_checklists.checklistcompartment",),
        ),
        migrations.AddConstraint(
            model_name="checklistcompartment",
            constraint=models.UniqueConstraint(
                condition=models.Q(("parent_compartment__isnull", True)),
                fields=("name", "parent_checklist"),
                name="name_is_unique_in_checklist",
            ),
        ),
        migrations.AddConstraint(
            model_name="checklistcompartment",
            constraint=models.UniqueConstraint(
                condition=models.Q(("parent_checklist__isnull", True)),
                fields=("name", "parent_compartment"),
                name="name_is_unique_in_compartment",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="checklistentry",
            unique_together={("compartment", "item_type")},
        ),
    ]
