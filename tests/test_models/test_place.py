#!/usr/bin/python3
"""Unittest module for the Place Class."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_forInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_for_no_argumentsInstantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_for_new_instance_storedIn_Obj(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_if_id_is_a_publicStrng(self):
        self.assertEqual(str, type(Place().id))

    def test_if_created_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_if_updated_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_if_city_id_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(plc))
        self.assertNotIn("city_id", plc.__dict__)

    def test_user_id_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(plc))
        self.assertNotIn("user_id", plc.__dict__)

    def test_name_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(plc))
        self.assertNotIn("name", plc.__dict__)

    def test_description_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(plc))
        self.assertNotIn("desctiption", plc.__dict__)

    def test_number_of_rooms_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(plc))
        self.assertNotIn("number_rooms", plc.__dict__)

    def test_number_of_bathrooms_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(plc))
        self.assertNotIn("number_bathrooms", plc.__dict__)

    def test_max_guest_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(plc))
        self.assertNotIn("max_guest", plc.__dict__)

    def test_price_by_night_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(plc))
        self.assertNotIn("price_by_night", plc.__dict__)

    def test_latitude_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(plc))
        self.assertNotIn("latitude", plc.__dict__)

    def test_longitude_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(plc))
        self.assertNotIn("longitude", plc.__dict__)

    def test_amenity_ids_is_a_public_classAttr(self):
        plc = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(plc))
        self.assertNotIn("amenity_ids", plc.__dict__)

    def test_if_two_places_has_uniqueId(self):
        plc1 = Place()
        plc2 = Place()
        self.assertNotEqual(plc1.id, plc2.id)

    def test_if_two_places_areDifferent_created_at(self):
        plc1 = Place()
        sleep(0.05)
        plc2 = Place()
        self.assertLess(plc1.created_at, plc2.created_at)

    def test_if_two_places_areDifferent_updated_at(self):
        plc1 = Place()
        sleep(0.05)
        plc2 = Place()
        self.assertLess(plc1.updated_at, plc2.updated_at)

    def test_for_stringRepr(self):
        dtime = datetime.today()
        dtime_repr = repr(dtime)
        plc = Place()
        plc.id = "123456"
        plc.created_at = plc.updated_at = dtime
        plcStr = plc.__str__()
        self.assertIn("[Place] (123456)", plcStr)
        self.assertIn("'id': '123456'", plcStr)
        self.assertIn("'created_at': " + dtime_repr, plcStr)
        self.assertIn("'updated_at': " + dtime_repr, plcStr)

    def test_if_args_areUnused(self):
        plc = Place(None)
        self.assertNotIn(None, plc.__dict__.values())

    def test_if_instantiation_has_kwargs(self):
        dtime = datetime.today()
        dtime_iso = dtime.isoformat()
        plc = Place(id="345", created_at=dtime_iso, updated_at=dtime_iso)
        self.assertEqual(plc.id, "345")
        self.assertEqual(plc.created_at, dtime)
        self.assertEqual(plc.updated_at, dtime)

    def test_for_instantiation_with_noKwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_forSave(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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
        plc = Place()
        sleep(0.05)
        firstUpdate_at = plc.updated_at
        plc.save()
        self.assertLess(firstUpdate_at, plc.updated_at)

    def test_for_twoSaves(self):
        plc = Place()
        sleep(0.05)
        firstUpdate_at = plc.updated_at
        plc.save()
        secondUpdate_at = plc.updated_at
        self.assertLess(firstUpdate_at, secondUpdate_at)
        sleep(0.05)
        plc.save()
        self.assertLess(secondUpdate_at, plc.updated_at)

    def test_for_save_with_argument(self):
        plc = Place()
        with self.assertRaises(TypeError):
            plc.save(None)

    def test_if_save_updatesFile(self):
        plc = Place()
        plc.save()
        plcId = "Place." + plc.id
        with open("file.json", "r") as f:
            self.assertIn(plcId, f.read())


class TestPlace_to_dict_function(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_the_to_dictType(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_if_to_dict_has_correctKeys(self):
        plc = Place()
        self.assertIn("id", plc.to_dict())
        self.assertIn("created_at", plc.to_dict())
        self.assertIn("updated_at", plc.to_dict())
        self.assertIn("__class__", plc.to_dict())

    def test_if_to_dict_has_addedAttr(self):
        plc = Place()
        plc.middleName = "Holberton"
        plc.my_number = 98
        self.assertEqual("Holberton", plc.middleName)
        self.assertIn("my_number", plc.to_dict())

    def test_if_to_dict_datetime_attr_areStrings(self):
        plc = Place()
        plcDict = plc.to_dict()
        self.assertEqual(str, type(plcDict["id"]))
        self.assertEqual(str, type(plcDict["created_at"]))
        self.assertEqual(str, type(plcDict["updated_at"]))

    def test_the_to_dictOutput(self):
        dtime = datetime.today()
        plc = Place()
        plc.id = "123456"
        plc.created_at = plc.updated_at = dtime
        tDict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat(),
        }
        self.assertDictEqual(plc.to_dict(), tDict)

    def test_is_contrast_to_dict_dunderDict(self):
        plc = Place()
        self.assertNotEqual(plc.to_dict(), plc.__dict__)

    def test_the_to_dict_with_argument(self):
        plc = Place()
        with self.assertRaises(TypeError):
            plc.to_dict(None)


if __name__ == "__main__":
    unittest.main()
