#!/usr/bin/python3
""" Defines unittests for amenity.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_for_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_for_no_argument_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_for_new_instance_stored_in_obj(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_if_id_is_a_public_string(self):
        self.assertEqual(str, type(Amenity().id))

    def test_for_created_at_is_publicDatetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_for_updated_at_is_publicDatetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_if_name_is_a_public_classAttribute(self):
        amnty = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amnty.__dict__)

    def test_for_two_amenities_uniqueId(self):
        amnty1 = Amenity()
        amnty2 = Amenity()
        self.assertNotEqual(amnty1.id, amnty2.id)

    def test_for_two_amenities_if_different_for_created_at(self):
        amnty1 = Amenity()
        sleep(0.05)
        amnty2 = Amenity()
        self.assertLess(amnty1.created_at, amnty2.created_at)

    def test_for_two_amenities_if_different_for_updated_at(self):
        amnty1 = Amenity()
        sleep(0.05)
        amnty2 = Amenity()
        self.assertLess(amnty1.updated_at, amnty2.updated_at)

    def test_for_a_string_representation(self):
        dtime = datetime.today()
        dtime_repr = repr(dtime)
        amnty = Amenity()
        amnty.id = "123456"
        amnty.created_at = amnty.updated_at = dtime
        amntystr = amnty.__str__()
        self.assertIn("[Amenity] (123456)", amntystr)
        self.assertIn("'id': '123456'", amntystr)
        self.assertIn("'created_at': " + dtime_repr, amntystr)
        self.assertIn("'updated_at': " + dtime_repr, amntystr)

    def test_for_unused_arguments(self):
        amnty = Amenity(None)
        self.assertNotIn(None, amnty.__dict__.values())

    def test_for_instantiation_withKwargs(self):
        """instantiation with kwargs test method"""
        dtime = datetime.today()
        dtime_iso = dtime.isoformat()
        amnty = Amenity(id="345", created_at=dtime_iso, updated_at=dtime_iso)
        self.assertEqual(amnty.id, "345")
        self.assertEqual(amnty.created_at, dtime)
        self.assertEqual(amnty.updated_at, dtime)

    def test_for_instantiation_with_No_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_for_saving(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_for_oneSave(self):
        amnty = Amenity()
        sleep(0.05)
        firstUpdated_at = amnty.updated_at
        amnty.save()
        self.assertLess(firstUpdated_at, amnty.updated_at)

    def test_for_twoSaves(self):
        amnty = Amenity()
        sleep(0.05)
        firstUpdated_at = amnty.updated_at
        amnty.save()
        secondUpdated_at = amnty.updated_at
        self.assertLess(firstUpdated_at, secondUpdated_at)
        sleep(0.05)
        amnty.save()
        self.assertLess(secondUpdated_at, amnty.updated_at)

    def test_for_saving_with_argument(self):
        amnty = Amenity()
        with self.assertRaises(TypeError):
            amnty.save(None)

    def test_for_save_updatesFile(self):
        amnty = Amenity()
        amnty.save()
        amntyId = "Amenity." + amnty.id
        with open("file.json", "r") as f:
            self.assertIn(amntyId, f.read())


class TestAmenity_to_dictionary(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dictionaryType(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dictionary_containing_correctKeys(self):
        amnty = Amenity()
        self.assertIn("id", amnty.to_dict())
        self.assertIn("created_at", amnty.to_dict())
        self.assertIn("updated_at", amnty.to_dict())
        self.assertIn("__class__", amnty.to_dict())

    def test_to_dict_containing_addedAttributes(self):
        amnty = Amenity()
        amnty.middleName = "Holberton"
        amnty.myNumber = 98
        self.assertEqual("Holberton", amnty.middleName)
        self.assertIn("myNumber", amnty.to_dict())

    def test_to_dict_datetime_if_attr_areStrings(self):
        amnty = Amenity()
        amnty_dict = amnty.to_dict()
        self.assertEqual(str, type(amnty_dict["id"]))
        self.assertEqual(str, type(amnty_dict["created_at"]))
        self.assertEqual(str, type(amnty_dict["updated_at"]))

    def test_to_dict_for_output(self):
        dtime = datetime.today()
        amnty = Amenity()
        amnty.id = "123456"
        amnty.created_at = amnty.updated_at = dtime
        tDict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat(),
        }
        self.assertDictEqual(amnty.to_dict(), tDict)

    def test_for_contrast_to_dict_dunderDict(self):
        amnty = Amenity()
        self.assertNotEqual(amnty.to_dict(), amnty.__dict__)

    def test_for_to_dict_with_argument(self):
        amnty = Amenity()
        with self.assertRaises(TypeError):
            amnty.to_dict(None)


if __name__ == "__main__":
    unittest.main()
