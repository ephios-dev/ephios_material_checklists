from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ephios_material_checklists.models.itemtype import ItemTypeCategory, ItemType


class MaterialItemGroupTypeTestCase(TestCase):

    # Attribute 'name'

    def test_item_type_category_requires_name_attribute(self):
        with self.assertRaises(Exception):
            category = ItemTypeCategory.objects.create(order_key=1)
            category.full_clean()

    def test_item_type_category_name_is_unique(self):
        this_category = ItemTypeCategory.objects.create(name="unique")
        this_category.full_clean()
        with self.assertRaises(Exception):
            other_category = ItemTypeCategory.objects.create(name="unique")
            other_category.full_clean()

    # Attribute 'order key'

    def test_item_type_category_order_key_is_always_similar_by_default(self):
        try:
            category_1 = ItemTypeCategory.objects.create(name="x")
            category_1.full_clean()
            category_2 = ItemTypeCategory.objects.create(name="y")
            category_2.full_clean()
        except Exception:
            self.fail("It should be possible to create an item type category without 'order key' attribute.")
        self.assertEqual(category_1.order_key, category_2.order_key,
                         "New item type categorys should have similar order key by default.")

    # String representation

    def test_item_type_category_string_representation(self):
        this_category = ItemTypeCategory.objects.create(name="Group")
        self.assertIn("Group", str(this_category), "Group name should be in item type category string representation.")



class MaterialItemTypeTestCase(TestCase):

    def setUp(self):
        self.category = ItemTypeCategory.objects.create(name="category")

    # Attribute 'name'

    def test_item_type_requires_name_attribute(self):
        with self.assertRaises(Exception):
            item = ItemType.objects.create(category=self.category)
            item.full_clean()

    def test_item_type_name_is_not_empty(self):
        with self.assertRaises(Exception):
            item = ItemType.objects.create(name="", category=self.category)
            item.full_clean()

    def test_item_type_name_is_unique(self):
        with self.assertRaises(Exception):
            category_1 = ItemTypeCategory.objects.create(name="A")
            item_1 = ItemType.objects.create(name="duplicate", category=category_1)
            item_1.full_clean()
            category_2 = ItemTypeCategory.objects.create(name="B")
            item_2 = ItemType.objects.create(name="duplicate", category=category_2)
            item_2.full_clean()

    # Attribute 'category'

    def test_item_type_requires_category_attribute(self):
        with self.assertRaises(Exception):
            item = ItemType.objects.create(name="xxx")
            item.full_clean()

    # Attribute 'notes'

    def test_item_type_notes_are_empty_by_default(self):
        try:
            item = ItemType.objects.create(name="name", category=self.category)
            item.full_clean()
        except Exception:
            self.fail("It should be possible to create an item type without 'notes' attribute.")
        self.assertEquals("", item.notes, "New item type note should be empty text by default.")

    # Attribute 'deprecated'

    def test_item_type_deprecated_is_false_by_default(self):
        try:
            item = ItemType.objects.create(name="name", category=self.category)
            item.full_clean()
        except Exception:
            self.fail("It should be possible to create an item type without 'deprecated' attribute.")
        self.assertFalse(item.deprecated, "New item type should not be deprecated by default.")

    # String representation 'notes'

    def test_item_type_string_representation(self):
        item = ItemType.objects.create(name="name", category=self.category)
        self.assertIn("name", str(item), "Item Type unformatted name should be in item type string repr.")
        self.assertNotIn("category", str(item), "Group name should NOT be in item type string representation.")
