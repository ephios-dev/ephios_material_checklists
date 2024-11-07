from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ephios_material_checklists.models.itemtype import ItemTypeCategory, ItemType


class ItemTypeCategoryTestCase(TestCase):

    # Attribute 'name'

    def test_item_type_category_requires_name_attribute(self):
        with self.assertRaises(Exception):
            category = ItemTypeCategory.objects.create(order_key=1)
            category.full_clean()
            self.fail(
                "It should not be possible to create an item type category without a name."
            )

    def test_item_type_category_name_is_unique(self):
        this_category = ItemTypeCategory.objects.create(name="unique")
        this_category.full_clean()
        with self.assertRaises(Exception):
            other_category = ItemTypeCategory.objects.create(name="unique")
            other_category.full_clean()
            self.fail(
                "It should not be possible to create an item type category with a name that is not unique."
            )

    # Attribute 'order key'

    def test_item_type_category_order_key_is_always_similar_by_default(self):
        try:
            category_1 = ItemTypeCategory.objects.create(name="x")
            category_1.full_clean()
            category_2 = ItemTypeCategory.objects.create(name="y")
            category_2.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create an item type category without 'order key' attribute."
            )
        self.assertEqual(
            category_1.order_key,
            category_2.order_key,
            "New item type categories should have similar order key by default.",
        )

    # String representation

    def test_item_type_category_string_representation(self):
        this_category = ItemTypeCategory.objects.create(name="Group")
        self.assertIn(
            "Group",
            str(this_category),
            "Group name should be in item type category string representation.",
        )


class ItemTypeTestCase(TestCase):

    def setUp(self):
        self.category = ItemTypeCategory.objects.create(name="category")

    # Attribute 'name'

    def test_item_type_requires_name_attribute(self):
        with self.assertRaises(Exception):
            item = ItemType.objects.create(category=self.category)
            item.full_clean()
            self.fail("It should not be possible to create an item type without name.")

    def test_item_type_name_is_not_empty(self):
        with self.assertRaises(Exception):
            item = ItemType.objects.create(name="", category=self.category)
            item.full_clean()
            self.fail(
                "It should not be possible to create an item type with empty name."
            )

    def test_item_type_name_is_unique(self):
        with self.assertRaises(Exception):
            category_1 = ItemTypeCategory.objects.create(name="A")
            item_1 = ItemType.objects.create(
                name="duplicate",
                category=category_1,
                has_expiry_date=False,
                deprecated=False,
            )
            item_1.full_clean()
            category_2 = ItemTypeCategory.objects.create(name="B")
            item_2 = ItemType.objects.create(
                name="duplicate",
                category=category_2,
                has_expiry_date=True,
                deprecated=False,
            )
            item_2.full_clean()
            self.fail(
                "It should not be possible to create an item type when one already exists with the same name."
            )

    # Attribute 'category'

    def test_item_type_requires_category_attribute(self):
        with self.assertRaises(Exception):
            item = ItemType.objects.create(
                name="xxx", has_expiry_date=True, deprecated=False
            )
            item.full_clean()
            self.fail(
                "It should not be possible to create an item type without a category."
            )

    # Attribute 'expiry date'

    def test_item_type_expiry_date_is_true_by_default(self):
        try:
            item = ItemType.objects.create(
                name="name", category=self.category, deprecated=True
            )
            item.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create an item type without 'has_expiry_date' attribute."
            )
        self.assertTrue(
            item.deprecated, "New item type should have expiry date by default."
        )

    # Attribute 'notes'

    def test_item_type_can_be_created_without_notes_attribute(self):
        try:
            item = ItemType.objects.create(
                name="name",
                category=self.category,
                has_expiry_date=True,
                deprecated=True,
            )
            item.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create an item type without 'notes' attribute."
            )

    def test_item_type_notes_are_empty_by_default(self):
        item = ItemType.objects.create(
            name="name",
            category=self.category,
            has_expiry_date=True,
            deprecated=True,
        )
        self.assertEquals(
            "", item.notes, "New item type note should be empty text by default."
        )

    # Attribute 'deprecated'

    def test_item_type_can_be_created_without_deprecation_attribute(self):
        try:
            item = ItemType.objects.create(
                name="name", category=self.category, has_expiry_date=True
            )
            item.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create an item type without 'deprecated' attribute."
            )

    def test_item_type_deprecated_is_false_by_default(self):
        item = ItemType.objects.create(
            name="name", category=self.category, has_expiry_date=True
        )
        self.assertFalse(
            item.deprecated, "New item type should not be deprecated by default."
        )

    # String representation 'notes'

    def test_item_type_string_representation(self):
        item = ItemType.objects.create(name="name", category=self.category)
        self.assertIn(
            "name",
            str(item),
            "Item Type name should be in item type string representation.",
        )
        self.assertNotIn(
            "category",
            str(item),
            "Category name should NOT be in item type string representation.",
        )

    # Attribute 'image'

    def test_item_type_can_be_created_without_image(self):
        try:
            item = ItemType.objects.create(
                name="name",
                category=self.category,
                has_expiry_date=True,
                deprecated=False,
            )
            item.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create an item type without 'image' attribute."
            )

    def test_item_type_image_is_empty_to_name_by_default(self):
        item = ItemType.objects.create(
            name="name",
            category=self.category,
            has_expiry_date=True,
            deprecated=False,
        )
        self.assertFalse(
            item.image, "New item type should not have an image by default."
        )

    def test_item_type_image_can_be_added(self):
        try:
            item = ItemType.objects.create(
                name="name",
                category=self.category,
                has_expiry_date=True,
                deprecated=False,
            )
            item.image = SimpleUploadedFile(
                "example_image.png",
                content=open(
                    "ephios_material_checklists/tests/files/example_image.png", "rb"
                ).read(),
                content_type="image/png",
            )
            item.save()
        except Exception:
            self.fail("It should be possible to add an image attribute for an item.")
        self.assertTrue(item.image, "After upload, item type should have an image.")

    def test_item_type_image_name(self):
        item = ItemType.objects.create(
            id=99,
            name="name",
            category=self.category,
            has_expiry_date=True,
            deprecated=False,
        )
        item.image = SimpleUploadedFile(
            "example_image.png",
            content=open(
                "ephios_material_checklists/tests/files/example_image.png", "rb"
            ).read(),
            content_type="image/png",
        )
        item.save()
        self.assertNotIn(
            "example_image",
            item.image.name,
            "Item type image name / path on server should not contain original upload filename anymore.",
        )
        self.assertIn(
            "item" + str(item.pk),
            item.image.name,
            'Item type image name / path on server should contain item type\'s id with prefix "item".',
        )
        # self.assertNotIn(
        #     str(self.category.pk),
        #     item.image.name,
        #     "Item type image name / path on server should not contain the category's id.",
        # )
        self.assertIn(
            "item_type/",
            item.image.name,
            'Item type image name / path on server should contain a folder "item_type/".',
        )
