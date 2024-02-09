#!/usr/bin/python3
"""Unittest module for the City Class."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_forInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_argumentInstantiates(self):
        self.assertEqual(City, type(City()))

    def test_newInstance_stored_inObj(self):
        self.assertIn(City(), models.storage.all().values())

    def test_if_id_is_a_publicString(self):
        self.assertEqual(str, type(City().id))

    def test_if_created_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_if_updated_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_if_state_id_is_a_public_classAttr(self):
        cty = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cty))
        self.assertNotIn("state_id", cty.__dict__)

    def test_if_name_is_a_public_classAttr(self):
        cty = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cty))
        self.assertNotIn("name", cty.__dict__)

    def test_for_two_cities_uniqueId(self):
        cty1 = City()
        cty2 = City()
        self.assertNotEqual(cty1.id, cty2.id)

    def test_for_two_cities_are_differentCreated_at(self):
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertLess(cty1.created_at, cty2.created_at)

    def test_for_two_cities_are_differentUpdated_at(self):
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertLess(cty1.updated_at, cty2.updated_at)

    def test_str_representation(self):
        dtime = datetime.today()
        dtime_repr = repr(dtime)
        cty = City()
        cty.id = "123456"
        cty.created_at = cty.updated_at = dtime
        ctyStrng = cty.__str__()
        self.assertIn("[City] (123456)", ctyStrng)
        self.assertIn("'id': '123456'", ctyStrng)
        self.assertIn("'created_at': " + dtime_repr, ctyStrng)
        self.assertIn("'updated_at': " + dtime_repr, ctyStrng)

    def test_for_unused_arguments(self):
        cty = City(None)
        self.assertNotIn(None, cty.__dict__.values())

    def test_for_instantiation_that_has_kwargs(self):
        dtime = datetime.today()
        dtime_iso = dtime.isoformat()
        cty = City(id="345", created_at=dtime_iso, updated_at=dtime_iso)
        self.assertEqual(cty.id, "345")
        self.assertEqual(cty.created_at, dtime)
        self.assertEqual(cty.updated_at, dtime)

    def test_for_instantiation_with_no_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_forSave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def prepare(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def cleanUp(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_for_oneSave(self):
        cty = City()
        sleep(0.05)
        firstUpdated_at = cty.updated_at
        cty.save()
        self.assertLess(firstUpdated_at, cty.updated_at)

    def test_for_twoSaves(self):
        cty = City()
        sleep(0.05)
        firstUpdated_at = cty.updated_at
        cty.save()
        secondUpdated_at = cty.updated_at
        self.assertLess(firstUpdated_at, secondUpdated_at)
        sleep(0.05)
        cty.save()
        self.assertLess(secondUpdated_at, cty.updated_at)

    def test_for_save_withArgument(self):
        cty = City()
        with self.assertRaises(TypeError):
            cty.save(None)

    def test_for_save_and_updatesFile(self):
        cty = City()
        cty.save()
        ctyId = "City." + cty.id
        with open("file.json", "r") as f:
            self.assertIn(ctyId, f.read())


class TestCity_for_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_for_to_dictType(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_if_to_dict_has_correctKeys(self):
        cty = City()
        self.assertIn("id", cty.to_dict())
        self.assertIn("created_at", cty.to_dict())
        self.assertIn("updated_at", cty.to_dict())
        self.assertIn("__class__", cty.to_dict())

    def test_if_to_dict_has_addedAttr(self):
        cty = City()
        cty.middle_name = "Holberton"
        cty.my_number = 98
        self.assertEqual("Holberton", cty.middle_name)
        self.assertIn("my_number", cty.to_dict())

    def test_if_to_dict_datetime_attr_areStrngs(self):
        cty = City()
        cty_dict = cty.to_dict()
        self.assertEqual(str, type(cty_dict["id"]))
        self.assertEqual(str, type(cty_dict["created_at"]))
        self.assertEqual(str, type(cty_dict["updated_at"]))

    def test_for_to_dictOutput(self):
        dtime = datetime.today()
        cty = City()
        cty.id = "123456"
        cty.created_at = cty.updated_at = dtime
        tDict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat(),
        }
        self.assertDictEqual(cty.to_dict(), tDict)

    def test_for_contrast_to_dictDunderDict(self):
        cty = City()
        self.assertNotEqual(cty.to_dict(), cty.__dict__)

    def test_for_to_dict_that_has_argument(self):
        cty = City()
        with self.assertRaises(TypeError):
            cty.to_dict(None)


if __name__ == "__main__":
    unittest.main()
