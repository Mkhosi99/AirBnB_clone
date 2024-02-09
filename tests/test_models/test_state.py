#!/usr/bin/python3
"""Unittest module for the State Class."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_forInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_for_no_argumentInstantiates(self):
        self.assertEqual(State, type(State()))

    def test_for_new_instanceStored_inObj(self):
        self.assertIn(State(), models.storage.all().values())

    def test_if_id_is_a_publicString(self):
        self.assertEqual(str, type(State().id))

    def test_if_created_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_if_updated_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_if_name_is_public_a_classAttr(self):
        sta = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(sta))
        self.assertNotIn("name", sta.__dict__)

    def test_two_states_for_uniqueId(self):
        sta1 = State()
        sta2 = State()
        self.assertNotEqual(sta1.id, sta2.id)

    def test_for_two_states_if_different_for_created_at(self):
        sta1 = State()
        sleep(0.05)
        sta2 = State()
        self.assertLess(sta1.created_at, sta2.created_at)

    def test_for_two_states_if_different_for_updated_at(self):
        sta1 = State()
        sleep(0.05)
        sta2 = State()
        self.assertLess(sta1.updated_at, sta2.updated_at)

    def test_for_stringRepresentation(self):
        dtime = datetime.today()
        dtime_repr = repr(dtime)
        sta = State()
        sta.id = "123456"
        sta.created_at = sta.updated_at = dtime
        staStr = sta.__str__()
        self.assertIn("[State] (123456)", staStr)
        self.assertIn("'id': '123456'", staStr)
        self.assertIn("'created_at': " + dtime_repr, staStr)
        self.assertIn("'updated_at': " + dtime_repr, staStr)

    def test_for_unusedArguments(self):
        sta = State(None)
        self.assertNotIn(None, sta.__dict__.values())

    def test_for_instantiation_that_hasKwargs(self):
        dtm = datetime.today()
        dtm_iso = dtm.isoformat()
        sta = State(id="345", created_at=dtm_iso, updated_at=dtm_iso)
        self.assertEqual(sta.id, "345")
        self.assertEqual(sta.created_at, dtm)
        self.assertEqual(sta.updated_at, dtm)

    def test_for_instantiation_with_noKwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_forSave(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        sta = State()
        sleep(0.05)
        firstUpdate_at = sta.updated_at
        sta.save()
        self.assertLess(firstUpdate_at, sta.updated_at)

    def test_for_twoSaves(self):
        sta = State()
        sleep(0.05)
        firstUpdate_at = sta.updated_at
        sta.save()
        secondUpdate_at = sta.updated_at
        self.assertLess(firstUpdate_at, secondUpdate_at)
        sleep(0.05)
        sta.save()
        self.assertLess(secondUpdate_at, sta.updated_at)

    def test_for_save_withArgument(self):
        sta = State()
        with self.assertRaises(TypeError):
            sta.save(None)

    def test_for_save_and_updatesFile(self):
        sta = State()
        sta.save()
        staId = "State." + sta.id
        with open("file.json", "r") as f:
            self.assertIn(staId, f.read())


class TestState_for_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_for_to_dictType(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_for_to_dict_has_correct_keys(self):
        sta = State()
        self.assertIn("id", sta.to_dict())
        self.assertIn("created_at", sta.to_dict())
        self.assertIn("updated_at", sta.to_dict())
        self.assertIn("__class__", sta.to_dict())

    def test_if_to_dict_has_addedAttr(self):
        sta = State()
        sta.middleName = "Holberton"
        sta.my_number = 98
        self.assertEqual("Holberton", sta.middleName)
        self.assertIn("my_number", sta.to_dict())

    def test_if_to_dict_datetime_attr_areStrings(self):
        sta = State()
        staDict = sta.to_dict()
        self.assertEqual(str, type(staDict["id"]))
        self.assertEqual(str, type(staDict["created_at"]))
        self.assertEqual(str, type(staDict["updated_at"]))

    def test_for_to_dictOutput(self):
        dtime = datetime.today()
        sta = State()
        sta.id = "123456"
        sta.created_at = sta.updated_at = dtime
        tDict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat(),
        }
        self.assertDictEqual(sta.to_dict(), tDict)

    def test_for_contrast_to_dictDunderDict(self):
        sta = State()
        self.assertNotEqual(sta.to_dict(), sta.__dict__)

    def test_for_to_dict_withArgument(self):
        sta = State()
        with self.assertRaises(TypeError):
            sta.to_dict(None)


if __name__ == "__main__":
    unittest.main()
