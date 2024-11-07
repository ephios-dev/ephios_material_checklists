import datetime

from django.test import TestCase
from django.urls import reverse

from ..models import *

# TODO: Test for proper cascaded delete of whole checklists.


class ChecklistTestCase(TestCase):

    # def setUp(self):
    #     self.specification = MaterialSpecification.objects.create(name="ab", date_publication=datetime.date(2018, 1, 1))
    #     self.specification_list = MaterialSpecificationList.objects.create(name="xy", specification=self.specification)

    # name attribute => MANDATORY, UNIQUE

    def test_checklist_requires_name_attribute(self):
        with self.assertRaises(Exception):
            this_checklist = Checklist.objects.create()
            this_checklist.full_clean()

    def test_checklist_name_attribute_is_unique(self):
        this_checklist = Checklist.objects.create(name="unique")
        this_checklist.full_clean()
        with self.assertRaises(Exception):
            other_checklist = Checklist.objects.create(name="unique")
            other_checklist.full_clean()

    # TODO: allow for a future 'group' or 'date' attribute to also qualify checklist (together with name)

    # specification attribute => MANY-TO-MANY, OPTIONAL, EMPTY BY DEFAULT

    # def test_checklist_has_no_specification_by_default(self):
    #     try:
    #         this_checklist = Checklist.objects.create(name="checklist", deprecated=False, abstract=False)
    #         this_checklist.full_clean()
    #     except Exception:
    #         self.fail("It should be possible to create a checklist without a 'fulfilled specification list' attribute.")
    #     self.assertEqual(0, this_checklist.fulfilled_specification_lists.count(),
    #                      "A checklist's default list of fulfilled specification should be empty.")

    # def test_checklist_can_add_specification(self):
    #     this_checklist = Checklist.objects.create(name="checklist", deprecated=False, abstract=False)
    #     try:
    #         this_checklist.fulfilled_specification_lists.add(self.specification_list)
    #         this_checklist.save()
    #     except Exception:
    #         self.fail("It should be possible to add a fulfilled specification to a checklist.")
    #     self.assertIn(self.specification_list, this_checklist.fulfilled_specification_lists.all(),
    #                   "Added specification list should be part of the checklist's fulfilled specifications.")

    # def test_checklist_can_add_multiple_specifications(self):
    #     other_specification_list = MaterialSpecificationList.objects.create(name="12", specification=self.specification)
    #     this_checklist = Checklist.objects.create(name="checklist", deprecated=False, abstract=False)
    #     try:
    #         this_checklist.fulfilled_specification_lists.add(self.specification_list)
    #         this_checklist.fulfilled_specification_lists.add(other_specification_list)
    #         this_checklist.save()
    #     except Exception:
    #         self.fail("It should be possible to add a fulfilled specification to a checklist.")
    #     self.assertIn(self.specification_list, this_checklist.fulfilled_specification_lists.all(),
    #                   "Added specification list should be part of the checklist's fulfilled specifications.")
    #     self.assertIn(other_specification_list, this_checklist.fulfilled_specification_lists.all(),
    #                   "Added specification list should be part of the checklist's fulfilled specifications.")

    # deprecated attribute => OPTIONAL, FALSE BY DEFAULT

    def test_checklist_can_be_created_without_deprecation_attribute(self):
        try:
            this_checklist = Checklist.objects.create(name="checklist", abstract=False)
            this_checklist.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a checklist without a 'deprecated' attribute."
            )

    def test_checklist_is_not_deprecated_by_default(self):
        this_checklist = Checklist.objects.create(name="checklist", abstract=False)
        self.assertFalse(
            this_checklist.deprecated,
            "A checklist should not be deprecated by default.",
        )

    # abstract attribute => OPTIONAL, FALSE BY DEFAULT

    def test_checklist_is_not_abstract_by_default(self):
        try:
            this_checklist = Checklist.objects.create(
                name="checklist", deprecated=False
            )
            this_checklist.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a checklist without a 'abstract' attribute."
            )
        self.assertFalse(
            this_checklist.abstract, "A checklist's should not be abstract by default."
        )

    # Method get_absolute_url()

    # def test_checklist_get_absolute_url(self):
    #     this_checklist = Checklist.objects.create(name="x")
    #     self.assertEquals(
    #         this_checklist.get_absolute_url(),
    #         reverse("material:checklist_detail", kwargs={"pk": this_checklist.pk}),
    #         "Material checklist absolute URL should point to details page with object PK.",
    #     )


class ChecklistCompartmentTestCase(TestCase):

    def setUp(self):
        self.checklist = Checklist.objects.create(name="checklist")
        self.other_checklist = Checklist.objects.create(name="other checklist")
        self.compartment_1 = ChecklistCompartment.objects.create(
            name="compartment 1", parent_checklist=self.checklist
        )
        self.compartment_2 = ChecklistCompartment.objects.create(
            name="compartment 2", parent_checklist=self.checklist
        )

    # Test 'name' attribute

    def test_checklist_compartment_requires_name_attribute(self):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartment.objects.create(
                parent_checklist=self.checklist
            )
            compartment.full_clean()

    def test_checklist_compartment_name_is_unique_in_checklist(self):
        compartment_3 = ChecklistCompartment.objects.create(
            name="unique", parent_checklist=self.checklist
        )
        compartment_3.full_clean()
        with self.assertRaises(Exception):
            compartment_4 = ChecklistCompartment.objects.create(
                name="unique", parent_checklist=self.checklist
            )
            compartment_4.full_clean()

    def test_checklist_compartment_name_is_unique_in_compartment(self):
        compartment_3 = ChecklistCompartment.objects.create(
            name="unique", parent_compartment=self.compartment_1
        )
        compartment_3.full_clean()
        with self.assertRaises(Exception):
            compartment_4 = ChecklistCompartment.objects.create(
                name="unique", parent_compartment=self.compartment_1
            )
            compartment_4.full_clean()

    def test_checklist_compartment_name_is_not_unique_in_different_checklists(self):
        try:
            compartment_3 = ChecklistCompartment.objects.create(
                name="x", parent_checklist=self.checklist
            )
            compartment_3.full_clean()
            compartment_4 = ChecklistCompartment.objects.create(
                name="x", parent_checklist=self.other_checklist
            )
            compartment_4.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a compartments with the same name in different checklists."
            )

    def test_checklist_compartment_name_is_not_unique_in_different_compartments(self):
        try:
            compartment_3 = ChecklistCompartment.objects.create(
                name="same", parent_compartment=self.compartment_1
            )
            compartment_3.full_clean()
            compartment_4 = ChecklistCompartment.objects.create(
                name="same", parent_compartment=self.compartment_2
            )
            compartment_4.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a compartments with the same name in different compartments."
            )

    # Test 'parent_compartment' and 'parent_checklist' attributes

    def test_checklist_compartment_cannot_be_in_compartment_and_in_checklist(self):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartment.objects.create(
                name="abcdef",
                parent_checklist=self.checklist,
                parent_compartment=self.compartment_1,
            )
            compartment.full_clean()

    def test_checklist_compartment_must_be_in_compartment_or_in_checklist(self):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartment.objects.create(name="nowhere")
            compartment.full_clean()

    def test_checklist_compartment_in_checklist_has_empty_parent_compartment(self):
        try:
            compartment = ChecklistCompartment.objects.create(
                name="xyz", parent_checklist=self.checklist
            )
            compartment.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a external-checklist-compartment without parent compartment."
            )
        self.assertIsNone(
            compartment.parent_compartment,
            "Compartment in checklist should have no parent compartment.",
        )

    def test_checklist_compartment_in_compartment_has_empty_parent_checklist(self):
        try:
            compartment = ChecklistCompartment.objects.create(
                name="xyz", parent_compartment=self.compartment_1
            )
            compartment.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a external-checklist-compartment without parent checklist."
            )
        self.assertIsNone(
            compartment.parent_checklist,
            "Compartment in compartment should have no parent checklist.",
        )

    def test_checklist_compartment_parent_compartment_cannot_have_external_checklist(
        self,
    ):
        external_checklist = Checklist.objects.create(name="some other checklist")
        compartment_with_external_checklist = (
            ChecklistCompartmentWithExternalChecklist.objects.create(
                name="xyz",
                parent_compartment=self.compartment_1,
                external_checklist=external_checklist,
            )
        )
        with self.assertRaises(
            Exception,
            msg="It should NOT be possible to create sub-compartments for compartments "
            + "with external checklist.",
        ):
            compartment = ChecklistCompartment.objects.create(
                name="a", parent_compartment=compartment_with_external_checklist
            )
            compartment.full_clean()

    def test_checklist_compartment_parent_compartment_cannot_be_self(self):
        compartment = ChecklistCompartment.objects.create(
            name="xyz", parent_compartment=self.compartment_1
        )
        with self.assertRaises(
            Exception, msg="It should NOT be possible to put a compartment into itself."
        ):
            compartment.parent_compartment = compartment
            compartment.save()
            compartment.full_clean()

    def test_checklist_compartment_parent_compartment_cannot_be_own_parent(self):
        compartment_a = ChecklistCompartment.objects.create(
            name="1", parent_compartment=self.compartment_1
        )
        compartment_b = ChecklistCompartment.objects.create(
            name="2", parent_compartment=compartment_a
        )
        compartment_c = ChecklistCompartment.objects.create(
            name="3", parent_compartment=compartment_b
        )
        with self.assertRaises(
            Exception,
            msg="It should NOT be possible to create circular compartment hierachy.",
        ):
            compartment_a.parent_compartment = compartment_c
            compartment_a.save()
            compartment_a.full_clean()

    # ChecklistCompartmentWithExternalChecklist.has_external_checklist()

    def test_checklist_compartment_in_checklist_has_external_checklist(self):
        compartment = ChecklistCompartment.objects.create(
            name="abc", parent_checklist=self.checklist
        )
        self.assertFalse(
            compartment.has_external_checklist(),
            "This compartment should have no external checklist.",
        )

    def test_checklist_compartment_in_compartment_has_external_checklist(self):
        compartment = ChecklistCompartment.objects.create(
            name="xyz", parent_compartment=self.compartment_1
        )
        self.assertFalse(
            compartment.has_external_checklist(),
            "This compartment should have no external checklist.",
        )

    # Test string representation ('__str__' method)

    def test_string_representation_in_compartment(self):
        compartment = ChecklistCompartment.objects.create(
            name="NAME", parent_compartment=self.compartment_1
        )
        self.assertIn(
            "checklist",
            str(compartment),
            "String representation should contain overall checklist name.",
        )
        self.assertIn(
            "compartment 1",
            str(compartment),
            "String representation should contain parent compartment n.",
        )
        self.assertIn(
            "NAME",
            str(compartment),
            "String representation should contain compartment name.",
        )

    def test_string_representation_in_checklist(self):
        compartment = ChecklistCompartment.objects.create(
            name="NAME", parent_checklist=self.checklist
        )
        self.assertIn(
            "checklist",
            str(compartment),
            "String representation should contain overall checklist name.",
        )
        self.assertIn(
            "NAME",
            str(compartment),
            "String representation should contain compartment name.",
        )


class ChecklistCompartmentWithExternalChecklistTestCase(TestCase):

    def setUp(self):
        self.checklist = Checklist.objects.create(name="checklist")
        self.compartment_1 = ChecklistCompartment.objects.create(
            name="comp 1", parent_checklist=self.checklist
        )

        self.other_checklist = Checklist.objects.create(name="other cl")
        self.other_checklist_compartment = ChecklistCompartment.objects.create(
            name="compartment", parent_checklist=self.other_checklist
        )

    # Test 'name' attribute

    def test_checklist_compartment_with_external_checklist_requires_name_attribute(
        self,
    ):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                parent_compartment=self.compartment_1,
                external_checklist=self.other_checklist,
            )
            compartment.full_clean()

    # Test 'external_checklist' attribute

    def test_checklist_compartment_with_external_checklist_requires_external_checklist_attribute(
        self,
    ):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                parent_compartment=self.compartment_1, name="bla bla bla"
            )
            compartment.full_clean()

    def test_checklist_compartment_with_external_checklist_checklist_cannot_be_parent_checklist(
        self,
    ):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                name="X",
                parent_checklist=self.checklist,
                external_checklist=self.checklist,
            )
            compartment.full_clean()

    def test_checklist_compartment_with_external_checklist_checklist_cannot_be_parent_compartment_checklist(
        self,
    ):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                name="X",
                parent_compartment=self.compartment_1,
                external_checklist=self.checklist,
            )
            compartment.full_clean()

    def test_checklist_compartment_with_external_checklist_checklist_must_be_unique(
        self,
    ):
        compartment_1 = ChecklistCompartmentWithExternalChecklist.objects.create(
            name="x",
            parent_compartment=self.compartment_1,
            external_checklist=self.other_checklist,
        )
        with self.assertRaises(
            Exception,
            msg="It should NOT be possible reference the same external checklist twice in a list.",
        ):
            compartment_2 = ChecklistCompartmentWithExternalChecklist.objects.create(
                name="c",
                parent_compartment=self.compartment_1,
                external_checklist=self.other_checklist,
            )

    # Test 'parent_compartment' and 'parent_checklist' attributes

    def test_checklist_compartment_with_external_checklist_cannot_be_in_compartment_and_in_checklist(
        self,
    ):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                name="W",
                parent_checklist=self.checklist,
                parent_compartment=self.compartment_1,
                external_checklist=self.other_checklist,
            )
            compartment.full_clean()

    def test_checklist_compartment_with_external_checklist_must_be_in_compartment_or_in_checklist(
        self,
    ):
        with self.assertRaises(Exception):
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                name="Z", external_checklist=self.other_checklist
            )
            compartment.full_clean()

    def test_checklist_compartment_with_external_checklist_in_checklist_has_empty_parent_compartment(
        self,
    ):
        try:
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                name="Y",
                parent_checklist=self.checklist,
                external_checklist=self.other_checklist,
            )
            compartment.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a external-checklist-compartment without parent compartment."
            )
        self.assertIsNone(
            compartment.parent_compartment,
            "Compartment in checklist should have no parent compartment.",
        )

    def test_checklist_compartment_with_external_checklist_in_compartment_has_empty_parent_checklist(
        self,
    ):
        try:
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                name="X",
                parent_compartment=self.compartment_1,
                external_checklist=self.other_checklist,
            )
            compartment.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a external-checklist-compartment without parent checklist."
            )
        self.assertIsNone(
            compartment.parent_checklist,
            "Compartment in checklist should have no parent checklist.",
        )

    def test_checklist_compartment_with_external_checklist_parent_compartment_cannot_have_external_checklist(
        self,
    ):
        external_checklist = Checklist.objects.create(name="some checklist")
        compartment_with_external_checklist = (
            ChecklistCompartmentWithExternalChecklist.objects.create(
                name="xyz",
                parent_compartment=self.compartment_1,
                external_checklist=external_checklist,
            )
        )
        with self.assertRaises(
            Exception,
            msg="It should NOT be possible to create sub-compartments for compartments "
            + "with external checklist.",
        ):
            compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
                name="abc",
                parent_compartment=compartment_with_external_checklist,
                external_checklist=self.other_checklist,
            )
            compartment.full_clean()

    def test_checklist_compartment_with_external_checklist_parent_compartment_cannot_be_self(
        self,
    ):
        compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
            name="abc",
            parent_compartment=self.compartment_1,
            external_checklist=self.other_checklist,
        )
        with self.assertRaises(
            Exception, msg="It should NOT be possible to put a compartment into itself."
        ):
            compartment.parent_compartment = compartment
            compartment.save()
            compartment.full_clean()

    # ChecklistCompartmentWithExternalChecklist.has_external_checklist()

    def test_checklist_compartment_with_external_checklist_in_checklist_has_external_checklist(
        self,
    ):
        compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
            name="abc",
            parent_checklist=self.checklist,
            external_checklist=self.other_checklist,
        )
        self.assertTrue(
            compartment.has_external_checklist(),
            "This compartment should have an external checklist.",
        )

    def test_checklist_compartment_with_external_checklist_in_compartment_has_external_checklist(
        self,
    ):
        compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
            name="xyz",
            parent_compartment=self.compartment_1,
            external_checklist=self.other_checklist,
        )
        self.assertTrue(
            compartment.has_external_checklist(),
            "This compartment should have an external checklist.",
        )

    # Test string representation ('__str__' method)

    def test_checklist_compartment_with_external_checklist_string_representation_in_compartment(
        self,
    ):
        compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
            name="NAME",
            parent_compartment=self.compartment_1,
            external_checklist=self.other_checklist,
        )
        self.assertIn(
            "checklist",
            str(compartment),
            "String representation should contain overall checklist name.",
        )
        self.assertIn(
            "comp 1",
            str(compartment),
            "String representation should contain parent compartment name.",
        )
        self.assertIn(
            "NAME",
            str(compartment),
            "String representation should contain local compartment name.",
        )
        self.assertIn(
            "other cl",
            str(compartment),
            "String representation should contain referenced checklist name.",
        )

    def test_checklist_compartment_with_external_checklist_string_representation_in_checklist(
        self,
    ):
        compartment = ChecklistCompartmentWithExternalChecklist.objects.create(
            name="NAME",
            parent_checklist=self.checklist,
            external_checklist=self.other_checklist,
        )
        self.assertIn(
            "checklist",
            str(compartment),
            "String representation should contain parent checklist name.",
        )
        self.assertIn(
            "NAME",
            str(compartment),
            "String representation should contain local compartment name.",
        )
        self.assertIn(
            "other cl",
            str(compartment),
            "String representation should contain referenced checklist name.",
        )


class ChecklistEntryTestCase(TestCase):

    def setUp(self):
        # Item type
        self.item_group = ItemTypeCategory.objects.create(name="Zeug")
        self.item = ItemType.objects.create(
            name="Sache", category=self.item_group
        )

        # Checklist with compartment
        self.checklist = Checklist.objects.create(name="checklist")
        self.compartment = ChecklistCompartment.objects.create(
            name="asdf", parent_checklist=self.checklist
        )

    # Test 'item_type' and 'compartment' attributes

    def test_checklist_entry_requires_item_type_attribute(self):
        with self.assertRaises(Exception):
            entry = ChecklistEntry.objects.create(
                amount=1, compartment=self.compartment
            )
            entry.full_clean()

    def test_checklist_entry_requires_compartment_attribute(self):
        with self.assertRaises(Exception):
            entry = ChecklistEntry.objects.create(item_type=self.item, amount=1)
            entry.full_clean()

    def test_checklist_entry_item_type_and_compartment_attributes_are_unique(self):
        entry_1 = ChecklistEntry.objects.create(
            item_type=self.item, compartment=self.compartment, amount=1
        )
        entry_1.full_clean()
        with self.assertRaises(Exception):
            entry_2 = ChecklistEntry.objects.create(
                item_type=self.item, compartment=self.compartment, amount=1
            )
            entry_2.full_clean()

    def test_checklist_entry_compartment_cannot_be_with_external_checklist(self):
        other_checklist = Checklist.objects.create(name="other checklist")
        compartment_with_external_checklist = (
            ChecklistCompartmentWithExternalChecklist.objects.create(
                name="reference to",
                parent_compartment=self.compartment,
                external_checklist=other_checklist,
            )
        )
        with self.assertRaises(
            Exception,
            msg="It should NOT be possible to create entry in compartment with external checklist.",
        ):
            entry = ChecklistEntry.objects.create(
                item_type=self.item,
                amount=1,
                compartment=compartment_with_external_checklist,
            )
            entry.full_clean()

    # Test 'amount' attribute

    def test_checklist_entry_requires_amount_attribute(self):
        with self.assertRaises(Exception):
            entry = ChecklistEntry.objects.create(
                item_type=self.item, compartment=self.compartment
            )
            entry.full_clean()

    def test_checklist_entry_amount_cannot_be_zero(self):
        with self.assertRaises(Exception):
            entry = ChecklistEntry.objects.create(
                item_type=self.item, compartment=self.compartment, amount=0
            )
            entry.full_clean()

    def test_checklist_entry_amount_cannot_be_below_zero(self):
        with self.assertRaises(Exception):
            entry = ChecklistEntry.objects.create(
                item_type=self.item, compartment=self.compartment, amount=-9
            )
            entry.full_clean()

    # Test 'optional' attribute

    def test_checklist_entry_is_not_optional_by_default(self):
        entry = ChecklistEntry.objects.create(
            item_type=self.item, compartment=self.compartment, amount=77
        )
        self.assertFalse(
            entry.optional, "New checklist entry should be non-optional by default."
        )
        try:
            entry.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create checklist entry without 'optional' attribute."
            )

    # Test 'notes' attribute

    def test_checklist_entry_can_be_created_without_notes_attribute(self):
        try:
            entry = ChecklistEntry.objects.create(
                item_type=self.item, compartment=self.compartment, amount=1
            )
            entry.full_clean()
        except Exception:
            self.fail(
                "It should be possible to create a checklist entry without notes attribute."
            )

    def test_checklist_entry_notes_attribute_is_empty_by_default(self):
        entry = ChecklistEntry.objects.create(
            item_type=self.item, compartment=self.compartment, amount=1
        )
        entry.full_clean()
        self.assertFalse(entry.notes, "Checklist entry notes should be empty by default.")

    # Test 'print_amount()' method

    def test_checklist_entry_text_print_amount_shows_normal_entry_amount_without_brackets(
        self,
    ):
        entry = ChecklistEntry.objects.create(
            item_type=self.item, compartment=self.compartment, amount=2
        )
        self.assertIn(
            "2",
            entry.print_amount(),
            "Checklist entry print_amount() should show amount value.",
        )
        self.assertNotIn(
            "[",
            entry.print_amount(),
            "Checklist entry print_amount() should normally NOT show brackets.",
        )
        self.assertNotIn(
            "]",
            entry.print_amount(),
            "Checklist entry print_amount() should normally NOT show brackets.",
        )

    def test_checklist_entry_text_print_amount_shows_optional_entry_amount_with_brackets(
        self,
    ):
        entry = ChecklistEntry.objects.create(
            item_type=self.item, compartment=self.compartment, amount=7, optional=True
        )
        self.assertIn(
            "7",
            entry.print_amount(),
            "Checklist entry print_amount() should show amount value.",
        )
        self.assertIn(
            "[",
            entry.print_amount(),
            "Checklist entry print_amount() should show brackets when optional.",
        )
        self.assertIn(
            "]",
            entry.print_amount(),
            "Checklist entry print_amount() should show brackets when optional.",
        )
        self.assertNotIn(
            "[7",
            entry.print_amount(),
            "Checklist entry print_amount() should NOT show brackets directly next to number.",
        )
        self.assertNotIn(
            "7]",
            entry.print_amount(),
            "Checklist entry print_amount() should NOT show brackets directly next to number.",
        )

    # Test string representation ('__str__' method)

    def test_string_representation(self):
        entry = ChecklistEntry.objects.create(
            item_type=self.item, compartment=self.compartment, amount=99
        )
        self.assertIn(
            self.item.name,
            str(entry),
            "String representation should contain item type name.",
        )
        self.assertIn(
            self.compartment.name,
            str(entry),
            "String representation should contain compartment name.",
        )
        self.assertIn("99", str(entry), "String representation should contain amount.")


class ChecklistAccessorTestCase(TestCase):

    def setUp(self):
        # Material Types
        self.item_category_1 = ItemTypeCategory.objects.create(name="Verbandmittel")
        self.item_11 = ItemType.objects.create(
            name="VP klein",
            category=self.item_category_1,
        )
        self.item_12 = ItemType.objects.create(
            name="VP groß", category=self.item_category_1
        )
        self.item_category_2 = ItemTypeCategory.objects.create(name="Infusionen")
        self.item_21 = ItemType.objects.create(
            name="Kanüle grün", category=self.item_category_2
        )
        self.item_22 = ItemType.objects.create(
            name="Infusion 500ml",
            category=self.item_category_2,
        )
        self.item_23 = ItemType.objects.create(
            name="Infusionssystem",
            category=self.item_category_2,
        )

        # External Checklist + Compartments
        self.external_checklist = Checklist.objects.create(name="external checklist")
        self.external_compartment = ChecklistCompartment.objects.create(
            name="external compartment", parent_checklist=self.external_checklist
        )
        self.external_sub_compartment = ChecklistCompartment.objects.create(
            name="external sub compartment",
            parent_compartment=self.external_compartment,
        )

        # Primary Checklist + Compartments
        self.this_checklist = Checklist.objects.create(name="checklist")
        self.compartment_1 = ChecklistCompartment.objects.create(
            name="1", parent_checklist=self.this_checklist
        )
        self.compartment_2 = ChecklistCompartment.objects.create(
            name="2", parent_checklist=self.this_checklist
        )
        self.compartment_21 = ChecklistCompartment.objects.create(
            name="21", parent_compartment=self.compartment_2
        )
        self.compartment_211 = ChecklistCompartment.objects.create(
            name="211", parent_compartment=self.compartment_21
        )
        self.compartment_22 = ChecklistCompartmentWithExternalChecklist.objects.create(
            name="22",
            parent_compartment=self.compartment_2,
            external_checklist=self.external_checklist,
        )

        # External Checklist + Compartments
        self.other_checklist = Checklist.objects.create(name="another checklist")
        self.other_compartment = ChecklistCompartment.objects.create(
            name="compartment", parent_checklist=self.other_checklist
        )

    # Checklist.get_compartments()

    def test_checklist_get_compartments_includes_directly_owned_compartments(self):
        self.assertIn(
            self.compartment_1,
            self.this_checklist.get_compartments(),
            "Checklist should contain this directly owned compartment.",
        )
        self.assertIn(
            self.compartment_2,
            self.this_checklist.get_compartments(),
            "Checklist should contain this directly owned compartment.",
        )

    def test_checklist_get_compartments_does_not_include_sub_compartments(self):
        self.assertNotIn(
            self.compartment_21,
            self.this_checklist.get_compartments(),
            "Checklist should NOT directly contain this sub-compartment.",
        )
        self.assertNotIn(
            self.compartment_211,
            self.this_checklist.get_compartments(),
            "Checklist should NOT directly contain this sub-compartment.",
        )
        self.assertNotIn(
            self.compartment_22,
            self.this_checklist.get_compartments(),
            "Checklist should NOT directly contain this sub-compartment.",
        )

    def test_checklist_get_compartments_does_not_include_compartments_from_external_checklist(
        self,
    ):
        self.assertNotIn(
            self.external_compartment,
            self.this_checklist.get_compartments(),
            "Checklist should NOT directly contain this compartment from the external checklist.",
        )
        self.assertNotIn(
            self.external_sub_compartment,
            self.this_checklist.get_compartments(),
            "Checklist should NOT directly contain this sub-compartment from the external checklist.",
        )

    def test_checklist_get_compartments_does_not_include_compartments_from_other_checklist(
        self,
    ):
        self.assertNotIn(
            self.other_compartment,
            self.this_checklist.get_compartments(),
            "Checklist should NOT directly contain this compartment from another checklist.",
        )

    # Checklist.get_all_compartments()

    def test_checklist_get_all_compartments_includes_directly_owned_compartments(self):
        self.assertIn(
            self.compartment_1,
            self.this_checklist.get_all_compartments(),
            "Checklist should contain this directly owned compartment.",
        )
        self.assertIn(
            self.compartment_2,
            self.this_checklist.get_all_compartments(),
            "Checklist should contain this directly owned compartment.",
        )

    def test_checklist_get_all_compartments_includes_sub_compartments(self):
        self.assertIn(
            self.compartment_21,
            self.this_checklist.get_all_compartments(),
            "Checklist should contain this sub-compartment.",
        )
        self.assertIn(
            self.compartment_211,
            self.this_checklist.get_all_compartments(),
            "Checklist should contain this sub-compartment.",
        )
        self.assertIn(
            self.compartment_22,
            self.this_checklist.get_all_compartments(),
            "Checklist should contain this sub-compartment.",
        )

    def test_checklist_get_all_compartments_includes_compartments_from_external_checklist(
        self,
    ):
        self.assertIn(
            self.external_compartment,
            self.this_checklist.get_all_compartments(),
            "Checklist should contain this compartment from an external checklist.",
        )
        self.assertIn(
            self.external_sub_compartment,
            self.this_checklist.get_all_compartments(),
            "Checklist should contain this sub-compartment from an external checklist.",
        )

    def test_checklist_get_all_compartments_does_not_include_compartments_from_other_checklist(
        self,
    ):
        self.assertNotIn(
            self.other_compartment,
            self.this_checklist.get_all_compartments(),
            "Checklist should NOT contain this compartment from another checklist.",
        )

    # Checklist.get_all_entries()

    def test_checklist_get_all_entries_includes_entries_from_directly_owned_compartments(
        self,
    ):
        entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=1, compartment=self.compartment_1
        )
        entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=2, compartment=self.compartment_2
        )
        self.assertIn(
            entry_1,
            self.this_checklist.get_all_entries(),
            "Checklist should contain this entry from a directly owned compartment.",
        )
        self.assertIn(
            entry_2,
            self.this_checklist.get_all_entries(),
            "Checklist should contain this entry from a directly owned compartment.",
        )

    def test_checklist_get_all_entries_includes_entries_from_sub_compartments(self):
        entry_21 = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=3, compartment=self.compartment_21
        )
        entry_211 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=4, compartment=self.compartment_211
        )
        self.assertIn(
            entry_21,
            self.this_checklist.get_all_entries(),
            "Checklist should contain this entry from a sub-compartment.",
        )
        self.assertIn(
            entry_211,
            self.this_checklist.get_all_entries(),
            "Checklist should contain this entry from a sub-sub-compartment.",
        )

    def test_checklist_get_all_entries_includes_entries_from_external_checklist(self):
        external_entry = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=5, compartment=self.external_compartment
        )
        external_sub_entry = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=6, compartment=self.external_sub_compartment
        )
        self.assertIn(
            external_entry,
            self.this_checklist.get_all_entries(),
            "Checklist should contain this entry from an external checklist.",
        )
        self.assertIn(
            external_sub_entry,
            self.this_checklist.get_all_entries(),
            "Checklist should contain this entry from an external checklist's sub-compartment.",
        )

    def test_checklist_get_all_entries_does_not_include_entries_from_other_checklist(
        self,
    ):
        other_entry = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=7, compartment=self.other_compartment
        )
        self.assertNotIn(
            other_entry,
            self.this_checklist.get_all_entries(),
            "Checklist should NOT contain this entry from another checklist.",
        )

    # Checklist.get_ordered_entries()

    def test_checklist_get_ordered_entries_includes_entries_from_directly_owned_compartments(
        self,
    ):
        entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=8, compartment=self.compartment_1
        )
        entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=9, compartment=self.compartment_2
        )
        self.assertIn(
            entry_1,
            self.this_checklist.get_ordered_entries(),
            "Checklist should contain this entry from a directly owned compartment.",
        )
        self.assertIn(
            entry_2,
            self.this_checklist.get_ordered_entries(),
            "Checklist should contain this entry from a directly owned compartment.",
        )

    def test_checklist_get_ordered_entries_includes_entries_from_sub_compartments(self):
        entry_21 = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=10, compartment=self.compartment_21
        )
        entry_211 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=11, compartment=self.compartment_211
        )
        self.assertIn(
            entry_21,
            self.this_checklist.get_ordered_entries(),
            "Checklist should contain this entry from a sub-compartment.",
        )
        self.assertIn(
            entry_211,
            self.this_checklist.get_ordered_entries(),
            "Checklist should contain this entry from a sub-sub-compartment.",
        )

    def test_checklist_get_ordered_entries_includes_entries_from_external_checklist(
        self,
    ):
        external_entry = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=12, compartment=self.external_compartment
        )
        external_sub_entry = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=13, compartment=self.external_sub_compartment
        )
        self.assertIn(
            external_entry,
            self.this_checklist.get_ordered_entries(),
            "Checklist should contain this entry from an external checklist.",
        )
        self.assertIn(
            external_sub_entry,
            self.this_checklist.get_ordered_entries(),
            "Checklist should contain this entry from an external checklist's sub-compartment.",
        )

    def test_checklist_get_ordered_entries_does_not_include_entries_from_other_checklist(
        self,
    ):
        other_entry = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=5, compartment=self.other_compartment
        )
        self.assertNotIn(
            other_entry,
            self.this_checklist.get_ordered_entries(),
            "Checklist should NOT contain this entry from another checklist.",
        )

    def test_checklist_get_ordered_entries_ordered_by_itemtype_group_and_name(self):
        # Create entries
        entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=3, compartment=self.compartment_211
        )
        entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=4, compartment=self.compartment_1
        )
        entry_3 = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=5, compartment=self.external_compartment
        )
        self.assertEquals(
            entry_1,
            self.this_checklist.get_ordered_entries()[0],
            "1st entry for specification should should be Infusionen (1st group) > Infusion (1st item).",
        )
        self.assertEquals(
            entry_2,
            self.this_checklist.get_ordered_entries()[1],
            "2nd entry for specification should should be Infusionen (1st group) > Kanüle (2nd item).",
        )
        self.assertEquals(
            entry_3,
            self.this_checklist.get_ordered_entries()[2],
            "3nd entry for specification should should be Verbandmittel (2nd group) > VP (only item).",
        )

    def test_specification_get_entries_ordered_by_itemtype_group_order_key(self):
        # Create entries
        entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=6, compartment=self.external_compartment
        )
        entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=7, compartment=self.compartment_21
        )
        entry_3 = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=8, compartment=self.external_compartment
        )

        # Overwrite order key of the item type groups
        self.item_category_1.order_key = 1000
        self.item_category_1.save()
        self.item_category_2.order_key = 1001
        self.item_category_2.save()

        # Entries should now be order by order key instead of name
        self.assertEquals(
            entry_1,
            self.this_checklist.get_ordered_entries()[0],
            "3nd entry for specification should should be Verbandmittel (2nd group) > VP (only item).",
        )
        self.assertEquals(
            entry_2,
            self.this_checklist.get_ordered_entries()[1],
            "1st entry for specification should should be Infusionen (1st group) > Infusion (1st item).",
        )
        self.assertEquals(
            entry_3,
            self.this_checklist.get_ordered_entries()[2],
            "2nd entry for specification should should be Infusionen (1st group) > Kanüle (2nd item).",
        )

    # Checklist.get_merged_entries()

    def test_checklist_get_merged_entries_merges_entries_from_different_directly_owned_compartments(
        self,
    ):
        ChecklistEntry.objects.create(
            item_type=self.item_12, amount=2, compartment=self.compartment_1
        )
        ChecklistEntry.objects.create(
            item_type=self.item_12, amount=1, compartment=self.compartment_2
        )
        self.assertTrue(
            any(
                [
                    e.item_type == self.item_12 and e.amount == 3
                    for e in self.this_checklist.get_merged_entries()
                ]
            ),
            "Checklist should merge entries with same item type that are in different owned compartments.",
        )

    def test_checklist_get_merged_entries_merges_entries_from_different_sub_compartments(
        self,
    ):
        ChecklistEntry.objects.create(
            item_type=self.item_22, amount=3, compartment=self.compartment_21
        )
        ChecklistEntry.objects.create(
            item_type=self.item_22, amount=2, compartment=self.compartment_211
        )
        self.assertTrue(
            any(
                [
                    e.item_type == self.item_22 and e.amount == 5
                    for e in self.this_checklist.get_merged_entries()
                ]
            ),
            "Checklist should merge entries with same item type that are in different owned compartments.",
        )

    def test_checklist_get_merged_entries_merges_entries_from_different_external_compartments(
        self,
    ):
        ChecklistEntry.objects.create(
            item_type=self.item_11, amount=4, compartment=self.external_compartment
        )
        ChecklistEntry.objects.create(
            item_type=self.item_11, amount=3, compartment=self.external_sub_compartment
        )
        self.assertTrue(
            any(
                [
                    e.item_type == self.item_11 and e.amount == 7
                    for e in self.this_checklist.get_merged_entries()
                ]
            ),
            "Checklist should merge entries with same item type from different external compartments.",
        )

    def test_checklist_get_merged_entries_merges_entries_from_directly_owned_compartment_and_sub_compartment(
        self,
    ):
        ChecklistEntry.objects.create(
            item_type=self.item_12, amount=4, compartment=self.compartment_2
        )
        ChecklistEntry.objects.create(
            item_type=self.item_12, amount=5, compartment=self.compartment_211
        )
        self.assertTrue(
            any(
                [
                    e.item_type == self.item_12 and e.amount == 9
                    for e in self.this_checklist.get_merged_entries()
                ]
            ),
            "Checklist should merge entries with same item type that are in different compartments.",
        )

    def test_checklist_get_merged_entries_merges_entries_from_directly_owned_compartment_and_external_compartment(
        self,
    ):
        ChecklistEntry.objects.create(
            item_type=self.item_22, amount=5, compartment=self.compartment_2
        )
        ChecklistEntry.objects.create(
            item_type=self.item_22, amount=6, compartment=self.external_compartment
        )
        self.assertTrue(
            any(
                [
                    e.item_type == self.item_22 and e.amount == 11
                    for e in self.this_checklist.get_merged_entries()
                ]
            ),
            "Checklist should merge entries with same item type that are in different compartments.",
        )

    def test_checklist_get_merged_entries_merges_entries_from_sub_compartment_and_external_compartment(
        self,
    ):
        ChecklistEntry.objects.create(
            item_type=self.item_23, amount=6, compartment=self.external_compartment
        )
        ChecklistEntry.objects.create(
            item_type=self.item_23, amount=7, compartment=self.compartment_21
        )
        self.assertTrue(
            any(
                [
                    e.item_type == self.item_23 and e.amount == 13
                    for e in self.this_checklist.get_merged_entries()
                ]
            ),
            "Checklist should merge entries with same item type that are in different compartments.",
        )

    def test_checklist_get_merged_entries_merges_entries_from_all_compartment_types(
        self,
    ):
        ChecklistEntry.objects.create(
            item_type=self.item_21, amount=11, compartment=self.compartment_2
        )
        ChecklistEntry.objects.create(
            item_type=self.item_21, amount=22, compartment=self.external_compartment
        )
        ChecklistEntry.objects.create(
            item_type=self.item_21, amount=33, compartment=self.compartment_211
        )
        self.assertTrue(
            any(
                [
                    e.item_type == self.item_21 and e.amount == 66
                    for e in self.this_checklist.get_merged_entries()
                ]
            ),
            "Checklist should merge entries with same item type that are in different compartments.",
        )

    def test_checklist_get_merged_entries_do_not_merge_entries_from_other_checklist(
        self,
    ):
        ChecklistEntry.objects.create(
            item_type=self.item_11, amount=10, compartment=self.external_compartment
        )
        ChecklistEntry.objects.create(
            item_type=self.item_11, amount=10, compartment=self.compartment_21
        )
        ChecklistEntry.objects.create(
            item_type=self.item_11, amount=10, compartment=self.compartment_1
        )
        ChecklistEntry.objects.create(
            item_type=self.item_11, amount=1000, compartment=self.other_compartment
        )
        self.assertFalse(
            any([e.amount >= 1000 for e in self.this_checklist.get_merged_entries()]),
            "Checklist should not merge entries from different checklist.",
        )

    def test_checklist_get_merged_entries_do_not_contain_original_entries_after_merge(
        self,
    ):
        entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=15, compartment=self.compartment_1
        )
        entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=15, compartment=self.compartment_2
        )
        entry_3 = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=22, compartment=self.compartment_211
        )
        entry_4 = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=22, compartment=self.external_compartment
        )
        entry_5 = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=22, compartment=self.compartment_21
        )
        self.assertNotIn(
            entry_1,
            self.this_checklist.get_merged_entries(),
            "Checklist should not contain original entry after merge happened for respective item type.",
        )
        self.assertNotIn(
            entry_2,
            self.this_checklist.get_merged_entries(),
            "Checklist should not contain original entry after merge happened for respective item type.",
        )
        self.assertNotIn(
            entry_3,
            self.this_checklist.get_merged_entries(),
            "Checklist should not contain original entry after merge happened for respective item type.",
        )
        self.assertNotIn(
            entry_4,
            self.this_checklist.get_merged_entries(),
            "Checklist should not contain original entry after merge happened for respective item type.",
        )
        self.assertNotIn(
            entry_5,
            self.this_checklist.get_merged_entries(),
            "Checklist should not contain original entry after merge happened for respective item type.",
        )

    def test_checklist_get_merged_entries_does_not_change_single_entries(self):
        entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=10, compartment=self.compartment_1
        )
        entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=11, compartment=self.compartment_2
        )
        entry_3 = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=12, compartment=self.compartment_211
        )
        entry_4 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=13, compartment=self.external_compartment
        )
        entry_5 = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=14, compartment=self.compartment_21
        )
        self.assertIn(
            entry_1,
            self.this_checklist.get_merged_entries(),
            "Checklist should not change entry during merge if there is no other entry with same item type.",
        )
        self.assertIn(
            entry_2,
            self.this_checklist.get_merged_entries(),
            "Checklist should not change entry during merge if there is no other entry with same item type.",
        )
        self.assertIn(
            entry_3,
            self.this_checklist.get_merged_entries(),
            "Checklist should not change entry during merge if there is no other entry with same item type.",
        )
        self.assertIn(
            entry_4,
            self.this_checklist.get_merged_entries(),
            "Checklist should not change entry during merge if there is no other entry with same item type.",
        )
        self.assertIn(
            entry_5,
            self.this_checklist.get_merged_entries(),
            "Checklist should not change entry during merge if there is no other entry with same item type.",
        )

    def test_checklist_get_merged_entries_ordered_by_itemtype_group_and_name(self):
        # Create entries (in random compartments)
        ChecklistEntry.objects.create(
            item_type=self.item_22, amount=3, compartment=self.compartment_1
        )
        ChecklistEntry.objects.create(
            item_type=self.item_22, amount=3, compartment=self.compartment_211
        )
        ChecklistEntry.objects.create(
            item_type=self.item_21, amount=3, compartment=self.external_sub_compartment
        )
        ChecklistEntry.objects.create(
            item_type=self.item_21, amount=4, compartment=self.compartment_1
        )
        ChecklistEntry.objects.create(
            item_type=self.item_12, amount=5, compartment=self.external_compartment
        )
        ChecklistEntry.objects.create(
            item_type=self.item_12, amount=5, compartment=self.compartment_2
        )

        # No order key of the item types => Entries should be ordered by group name
        self.assertEquals(
            self.item_22,
            self.this_checklist.get_merged_entries()[0].item_type,
            "1st entry for specification should should be Infusionen (1st group) > Infusion (1st item).",
        )
        self.assertEquals(
            self.item_21,
            self.this_checklist.get_merged_entries()[1].item_type,
            "2nd entry for specification should should be Infusionen (1st group) > Kanüle (2nd item).",
        )
        self.assertEquals(
            self.item_12,
            self.this_checklist.get_merged_entries()[2].item_type,
            "3nd entry for specification should should be Verbandmittel (2nd group) > VP (only item).",
        )

    def test_checklist_get_merged_ordered_by_itemtype_group_order_key(self):
        # Create entries (in random compartments)
        ChecklistEntry.objects.create(
            item_type=self.item_22, amount=8, compartment=self.external_compartment
        )
        ChecklistEntry.objects.create(
            item_type=self.item_22, amount=8, compartment=self.compartment_2
        )
        ChecklistEntry.objects.create(
            item_type=self.item_21, amount=8, compartment=self.compartment_211
        )
        ChecklistEntry.objects.create(
            item_type=self.item_21, amount=8, compartment=self.external_compartment
        )
        ChecklistEntry.objects.create(
            item_type=self.item_11, amount=8, compartment=self.compartment_1
        )
        ChecklistEntry.objects.create(
            item_type=self.item_11, amount=8, compartment=self.compartment_21
        )

        # Overwrite order key of the item type groups
        self.item_category_1.order_key = 1000
        self.item_category_1.save()
        self.item_category_2.order_key = 1001
        self.item_category_2.save()

        # Entries should now be order by order key instead of name
        self.assertEquals(
            self.item_11,
            self.this_checklist.get_merged_entries()[0].item_type,
            "3nd entry for specification should should be Verbandmittel (2nd group) > VP (only item).",
        )
        self.assertEquals(
            self.item_22,
            self.this_checklist.get_merged_entries()[1].item_type,
            "1st entry for specification should should be Infusionen (1st group) > Infusion (1st item).",
        )
        self.assertEquals(
            self.item_21,
            self.this_checklist.get_merged_entries()[2].item_type,
            "2nd entry for specification should should be Infusionen (1st group) > Kanüle (2nd item).",
        )

    # ChecklistCompartment.get_checklist()

    def test_checklist_compartment_get_checklist_from_directly_owned_compartments(self):
        self.assertEqual(
            self.this_checklist,
            self.compartment_1.checklist(),
            "Should find checklist for directly owned compartment.",
        )
        self.assertEqual(
            self.this_checklist,
            self.compartment_2.checklist(),
            "Should find checklist for directly owned compartment.",
        )

    def test_checklist_compartment_get_checklist_from_sub_compartments(self):
        self.assertEqual(
            self.this_checklist,
            self.compartment_21.checklist(),
            "Should find checklist for sub-compartment.",
        )
        self.assertEqual(
            self.this_checklist,
            self.compartment_211.checklist(),
            "Should find checklist for sub-sub-compartment.",
        )
        self.assertEqual(
            self.this_checklist,
            self.compartment_22.checklist(),
            "Should find checklist for sub-compartment.",
        )

    def test_checklist_compartment_get_checklist_from_external_compartments(self):
        self.assertEqual(
            self.external_checklist,
            self.external_compartment.checklist(),
            "Should find correct checklist for external compartment.",
        )
        self.assertNotEqual(
            self.this_checklist,
            self.external_compartment.checklist(),
            "Should not find primary checklist for external compartment.",
        )

    def test_checklist_compartment_get_checklist_from_other_compartments(self):
        self.assertEqual(
            self.other_checklist,
            self.other_compartment.checklist(),
            "Should find correct checklist for other compartment.",
        )
        self.assertNotEqual(
            self.this_checklist,
            self.other_compartment.checklist(),
            "Should not find primary checklist for other compartment.",
        )

    # ChecklistEntry.checklist()

    def test_checklist_entry_get_checklist_from_directly_owned_compartments(self):
        entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=8, compartment=self.compartment_1
        )
        entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=7, compartment=self.compartment_2
        )
        self.assertEqual(
            self.this_checklist,
            entry_1.checklist(),
            "Should find checklist for an entry in a directly owned compartment.",
        )
        self.assertEqual(
            self.this_checklist,
            entry_2.checklist(),
            "Should find checklist for an entry in a directly owned compartment.",
        )

    def test_checklist_entry_get_checklist_from_sub_compartments(self):
        entry_21 = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=6, compartment=self.compartment_1
        )
        entry_211 = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=5, compartment=self.compartment_2
        )
        self.assertEqual(
            self.this_checklist,
            entry_21.checklist(),
            "Should find checklist for an entry in a sub-compartment.",
        )
        self.assertEqual(
            self.this_checklist,
            entry_211.checklist(),
            "Should find checklist for an entry in a sub-sub-compartment.",
        )

    def test_checklist_entry_get_checklist_from_external_compartments(self):
        external_entry = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=4, compartment=self.external_compartment
        )
        self.assertEqual(
            self.external_checklist,
            external_entry.checklist(),
            "Should find correct checklist for an entry in an external compartment.",
        )
        self.assertNotEqual(
            self.this_checklist,
            external_entry.checklist(),
            "Should not find primary checklist for an entry in external compartment.",
        )

    def test_checklist_entry_get_checklist_from_other_compartments(self):
        other_entry = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=3, compartment=self.other_compartment
        )
        self.assertEqual(
            self.other_checklist,
            other_entry.checklist(),
            "Should find correct checklist for other compartment.",
        )
        self.assertNotEqual(
            self.this_checklist,
            other_entry.checklist(),
            "Should not find primary checklist for other compartment.",
        )

    # ChecklistCompartment.get_sub_compartments()

    def test_checklist_compartment_get_sub_compartments_empty_for_leaves(self):
        self.assertFalse(
            self.compartment_1.get_sub_compartments(),
            "This compartment should have no sub-compartments.",
        )
        self.assertFalse(
            self.compartment_211.get_sub_compartments(),
            "Compartment should not have sub-compartments.",
        )

    def test_checklist_compartment_get_sub_compartments_contains_valid_sub_compartments(
        self,
    ):
        self.assertIn(
            self.compartment_21,
            self.compartment_2.get_sub_compartments(),
            "This compartment should be a valid sub-compartments.",
        )
        self.assertIn(
            self.compartment_211,
            self.compartment_21.get_sub_compartments(),
            "This compartment should be a valid sub-compartments.",
        )

    def test_checklist_compartment_get_sub_compartments_does_not_contain_itself(self):
        self.assertNotIn(
            self.compartment_2,
            self.compartment_2.get_sub_compartments(),
            "The compartment itself not a valid sub-compartments.",
        )
        self.assertNotIn(
            self.compartment_21,
            self.compartment_21.get_sub_compartments(),
            "The compartment itself not a valid sub-compartments.",
        )

    def test_checklist_compartment_get_sub_compartments_does_not_contain_neighbours(
        self,
    ):
        self.assertNotIn(
            self.compartment_1,
            self.compartment_2.get_sub_compartments(),
            "A neighbouring compartment not a valid sub-compartments.",
        )

    def test_checklist_compartment_get_sub_compartments_does_not_contain_other_compartments(
        self,
    ):
        self.assertNotIn(
            self.other_compartment,
            self.compartment_2.get_sub_compartments(),
            "A totally different compartment not a valid sub-compartments.",
        )
        self.assertNotIn(
            self.other_compartment,
            self.compartment_21.get_sub_compartments(),
            "A totally different compartment not a valid sub-compartments.",
        )

    # ChecklistCompartmentWithExternalChecklist.get_sub_compartments()

    def test_checklist_compartment_with_external_checklist_get_sub_compartments(self):
        self.assertIn(
            self.external_compartment,
            self.compartment_22.get_sub_compartments(),
            "This top-level compartment is a valid sub-compartment of one that includes it's checklist.",
        )

    # ChecklistCompartment.get_local_entries()

    def test_checklist_compartment_get_local_entries(self):
        # Create some entries (for compartment_21)
        local_entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=8, compartment=self.compartment_21
        )
        local_entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=12, compartment=self.compartment_21
        )
        child_entry = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=1, compartment=self.compartment_211
        )
        parent_entry = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=2, compartment=self.compartment_2
        )
        other_entry = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=3, compartment=self.other_compartment
        )

        # Test that only local are retrieved
        self.assertIn(
            local_entry_1,
            self.compartment_21.get_local_entries(),
            "Compartment should contain local entry.",
        )
        self.assertIn(
            local_entry_2,
            self.compartment_21.get_local_entries(),
            "Compartment should contain local entry.",
        )
        self.assertNotIn(
            child_entry,
            self.compartment_21.get_local_entries(),
            "Compartment should not contain child entry.",
        )
        self.assertNotIn(
            parent_entry,
            self.compartment_21.get_local_entries(),
            "Compartment should not contain parent entry.",
        )
        self.assertNotIn(
            other_entry,
            self.compartment_21.get_local_entries(),
            "Compartment should not contain random other entry.",
        )

    # ChecklistCompartment.get_all_entries()

    def test_checklist_compartment_get_all_entries(self):
        # Create some entries (for compartment_21)
        local_entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=33, compartment=self.compartment_21
        )
        local_entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=23, compartment=self.compartment_21
        )
        child_entry = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=32, compartment=self.compartment_211
        )
        parent_entry = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=30, compartment=self.compartment_2
        )
        other_entry = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=29, compartment=self.other_compartment
        )

        # Test that local entries and entries from children are retrieved
        self.assertIn(
            local_entry_1,
            self.compartment_21.get_all_entries(),
            "Compartment should contain local entry.",
        )
        self.assertIn(
            local_entry_2,
            self.compartment_21.get_all_entries(),
            "Compartment should contain local entry.",
        )
        self.assertIn(
            child_entry,
            self.compartment_21.get_all_entries(),
            "Compartment should contain child entry.",
        )
        self.assertNotIn(
            parent_entry,
            self.compartment_21.get_all_entries(),
            "Compartment should not contain parent entry.",
        )
        self.assertNotIn(
            other_entry,
            self.compartment_21.get_all_entries(),
            "Compartment should not contain random other entry.",
        )

    # ChecklistCompartmentWithExternalChecklist.get_all_entries(self)

    def test_checklist_compartment_with_external_checklist_get_all_entries(self):
        # Create some entries
        external_entry = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=33, compartment=self.external_compartment
        )
        external_sub_entry = ChecklistEntry.objects.create(
            item_type=self.item_21, amount=23, compartment=self.external_sub_compartment
        )
        parent_entry = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=29, compartment=self.compartment_21
        )
        other_entry = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=29, compartment=self.other_compartment
        )

        # Test that local entries and entries from children are retrieved
        self.assertIn(
            external_entry,
            self.compartment_22.get_all_entries(),
            "Compartment should contain this entry from the referenced external checklist.",
        )
        self.assertIn(
            external_sub_entry,
            self.compartment_22.get_all_entries(),
            "Compartment should contain this entry from a sub-compartment of the external checklist.",
        )
        self.assertNotIn(
            parent_entry,
            self.compartment_22.get_all_entries(),
            "Compartment should not contain this entry from the parent checklist.",
        )
        self.assertNotIn(
            other_entry,
            self.compartment_22.get_all_entries(),
            "Compartment should not contain this entry from a random other checklist.",
        )

    # Test ChecklistCompartment.copy_content_from()

    def test_checklist_compartment_copy_contents_from_not_for_empty_checklist(self):
        self.assertEquals(
            2,
            len(self.compartment_2.get_sub_compartments()),
            "Compartment should have 2 sub-compartments.",
        )
        self.compartment_2.copy_content_from(self.other_compartment)
        self.assertEquals(
            2,
            len(self.compartment_2.get_sub_compartments()),
            "Compartment should have 2 sub-compartments after copy as well.",
        )

    # Test Checklist.copy_compartments_from()

    def test_checklist_copy_compartments_from_not_for_empty_checklist(self):
        self.assertEquals(
            2,
            len(self.this_checklist.get_compartments()),
            "Checklist should have 2 compartments.",
        )
        self.this_checklist.copy_compartments_from(self.other_checklist)
        self.assertEquals(
            2,
            len(self.this_checklist.get_compartments()),
            "Checklist should have 2 compartments after copy as well.",
        )

    def test_checklist_copy_compartments_from_creates_similar_compartments(self):
        # Create empty checklist and test that it actually is empty
        new_checklist = Checklist.objects.create(name="new and empty still")
        self.assertEquals(
            0,
            len(new_checklist.get_compartments()),
            "New checklist should be empty initially.",
        )
        self.assertEquals(
            0,
            len(new_checklist.get_all_entries()),
            "New checklist should be empty initially.",
        )

        # Copy checklist contents and test equal numbers
        new_checklist.copy_compartments_from(self.this_checklist)
        self.assertEquals(
            len(new_checklist.get_compartments()),
            len(self.this_checklist.get_compartments()),
            "Checklist after copy operation should contain as many compartments as source checklist.",
        )
        self.assertEquals(
            len(new_checklist.get_all_compartments()),
            len(self.this_checklist.get_all_compartments()),
            "Checklist after copy operation should contain as many compartments as source checklist.",
        )

        # Test that copied local compartment instances are not equal
        for compartment in [
            self.compartment_1,
            self.compartment_2,
            self.compartment_21,
            self.compartment_22,
            self.compartment_211,
        ]:
            self.assertNotIn(
                compartment,
                new_checklist.get_all_compartments(),
                "Local compartments of new checklist should NOT be (identical to those) in old checklist.",
            )

        # Test that copied external compartment instances are equal
        for compartment in [self.external_compartment, self.external_sub_compartment]:
            self.assertIn(
                compartment,
                new_checklist.get_all_compartments(),
                "External compartments of new checklist should be (identical to those) in old checklist.",
            )

        # Test that names and ordering of copies compartments are equal
        for i in range(0, len(new_checklist.get_all_compartments())):
            self.assertEqual(
                new_checklist.get_all_compartments()[i].name,
                self.this_checklist.get_all_compartments()[i].name,
                "Compartments of new and old checklists should have same names and ordering.",
            )

    def test_checklist_copy_compartments_from_creates_similar_entries(self):
        # Create some entries in various places
        local_entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_22, amount=13, compartment=self.compartment_1
        )
        local_entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=33, compartment=self.compartment_21
        )
        local_entry_3 = ChecklistEntry.objects.create(
            item_type=self.item_11, amount=99, compartment=self.compartment_211
        )
        external_entry_1 = ChecklistEntry.objects.create(
            item_type=self.item_12, amount=1, compartment=self.external_compartment
        )
        external_entry_2 = ChecklistEntry.objects.create(
            item_type=self.item_23, amount=4, compartment=self.external_sub_compartment
        )

        # Create empty checklist and test that it actually is empty
        new_checklist = Checklist.objects.create(name="brand new one")
        self.assertEquals(
            0,
            len(new_checklist.get_compartments()),
            "New checklist should initially be empty.",
        )
        self.assertEquals(
            0,
            len(new_checklist.get_all_entries()),
            "New checklist should initially be empty.",
        )

        # Copy checklist contents and test equal numbers
        new_checklist.copy_compartments_from(self.this_checklist)
        self.assertEquals(
            len(new_checklist.get_all_entries()),
            len(self.this_checklist.get_all_entries()),
            "Checklist after copy operation should contain as many total entries as source checklist.",
        )
        self.assertEquals(
            len(new_checklist.get_merged_entries()),
            len(self.this_checklist.get_merged_entries()),
            "Checklist after copy operation should contain as many merged entries as source checklist.",
        )

        # Test that copied local entry instances are not equal
        for entry in [local_entry_1, local_entry_2, local_entry_3]:
            self.assertNotIn(
                entry,
                new_checklist.get_all_entries(),
                "Local Entries of new checklist should NOT be (identical to those) in old checklist.",
            )

        # Test that copied external entry instances are indeed equal (since external checklist is the same)
        for entry in [external_entry_1, external_entry_2]:
            self.assertIn(
                entry,
                new_checklist.get_all_entries(),
                "External Entries of new checklist should be (identical to those) in old checklist.",
            )

        # Test that item_types, amounts and ordering of copies entries are equal
        for i in range(0, len(new_checklist.get_ordered_entries())):
            self.assertEqual(
                new_checklist.get_ordered_entries()[i].item_type,
                self.this_checklist.get_ordered_entries()[i].item_type,
                "Entries of new and old checklist should have same item types, amounts and ordering.",
            )
            self.assertEqual(
                new_checklist.get_ordered_entries()[i].amount,
                self.this_checklist.get_ordered_entries()[i].amount,
                "Entries of new and old checklist should have same item types, amounts and ordering.",
            )

        # Test that item_types, amounts and ordering of copies merged entries are equal
        for i in range(0, len(new_checklist.get_merged_entries())):
            self.assertEqual(
                new_checklist.get_merged_entries()[i].item_type,
                self.this_checklist.get_merged_entries()[i].item_type,
                "Entries of new and old checklist should have same item types, amounts and ordering.",
            )
            self.assertEqual(
                new_checklist.get_merged_entries()[i].amount,
                self.this_checklist.get_merged_entries()[i].amount,
                "Entries of new and old checklist should have same item types, amounts and ordering.",
            )
