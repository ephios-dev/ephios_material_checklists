# Generated by Django 5.0.9 on 2024-11-06 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ItemTypeCategory",
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
                    "order_key",
                    models.IntegerField(default=1, verbose_name="ordering index"),
                ),
            ],
            options={
                "verbose_name": "item type category",
                "verbose_name_plural": "item type categories",
                "ordering": ("order_key", "name"),
            },
        ),
        migrations.CreateModel(
            name="ItemType",
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
                    "has_expiry_date",
                    models.BooleanField(default=True, verbose_name="has expiry date"),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "deprecated",
                    models.BooleanField(default=False, verbose_name="deprecated"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="ephios_material_checklists.itemtypecategory",
                        verbose_name="category",
                    ),
                ),
            ],
            options={
                "verbose_name": "item type",
                "verbose_name_plural": "item types",
                "ordering": ("category__order_key", "category__name", "name"),
            },
        ),
    ]
