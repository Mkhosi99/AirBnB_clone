#!/usr/bin/python3
"""Unittest module for the User Class."""
import os
import models
from models.user import User
import unittest
from datetime import datetime
from time import sleep


class TestUser_forInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_for_no_argumentInstantiates(self):
        self.assertEqual(User, type(User()))

    def test_for_new_instance_stored_inObj(self):
        self.assertIn(User(), models.storage.all().values())

    def test_if_id_is_a_public_string(self):
        self.assertEqual(str, type(User().id))

    def test_if_created_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_if_updated_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_if_email_is_a_publicString(self):
        self.assertEqual(str, type(User.email))

    def test_if_password_is_a_publicString(self):
        self.assertEqual(str, type(User.password))

    def test_if_first_name_is_a_publicString(self):
        self.assertEqual(str, type(User.first_name))

    def test_if_last_name_is_a_publicString(self):
        self.assertEqual(str, type(User.last_name))

    def test_for_two_users_uniqueId(self):
        usr1 = User()
        usr2 = User()
        self.assertNotEqual(usr1.id, usr2.id)

    def test_if_two_users_are_different_for_created_at(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.created_at, usr2.created_at)

    def test_if_two_users_are_different_for_updated_at(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.updated_at, usr2.updated_at)

    def test_forString_repr(self):
        dtime = datetime.today()
        dtime_repr = repr(dtime)
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = dtime
        usrStr = usr.__str__()
        self.assertIn("[User] (123456)", usrStr)
        self.assertIn("'id': '123456'", usrStr)
        self.assertIn("'created_at': " + dtime_repr, usrStr)
        self.assertIn("'updated_at': " + dtime_repr, usrStr)

    def test_for_unused_argument(self):
        usr = User(None)
        self.assertNotIn(None, usr.__dict__.values())

    def test_for_instantiation_that_hasKwargs(self):
        dtime = datetime.today()
        dtime_iso = dtime.isoformat()
        usr = User(id="345", created_at=dtime_iso, updated_at=dtime_iso)
        self.assertEqual(usr.id, "345")
        self.assertEqual(usr.created_at, dtime)
        self.assertEqual(usr.updated_at, dtime)

    def test_forInstantiation_with_noKwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_forSave(unittest.TestCase):
    """Unittests for testing save method of the  class."""

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
        usr = User()
        sleep(0.05)
        firstUpdate_at = usr.updated_at
        usr.save()
        self.assertLess(firstUpdate_at, usr.updated_at)

    def test_for_twoSaves(self):
        usr = User()
        sleep(0.05)
        firstUpdate_at = usr.updated_at
        usr.save()
        secondUpdate_at = usr.updated_at
        self.assertLess(firstUpdate_at, secondUpdate_at)
        sleep(0.05)
        usr.save()
        self.assertLess(secondUpdate_at, usr.updated_at)

    def test_for_save_withArgument(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.save(None)

    def test_for_save_and_updatesFile(self):
        usr = User()
        usr.save()
        usrId = "User." + usr.id
        with open("file.json", "r") as f:
            self.assertIn(usrId, f.read())


class TestUser_for_toDict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_for_to_dictType(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_if_to_dict_has_correctKeys(self):
        usr = User()
        self.assertIn("id", usr.to_dict())
        self.assertIn("created_at", usr.to_dict())
        self.assertIn("updated_at", usr.to_dict())
        self.assertIn("__class__", usr.to_dict())

    def test_if_to_dict_has_addedAttr(self):
        usr = User()
        usr.middleName = "Holberton"
        usr.my_number = 98
        self.assertEqual("Holberton", usr.middleName)
        self.assertIn("my_number", usr.to_dict())

    def test_if_to_dict_datetimeAttr_are_strings(self):
        usr = User()
        usrDict = usr.to_dict()
        self.assertEqual(str, type(usrDict["id"]))
        self.assertEqual(str, type(usrDict["created_at"]))
        self.assertEqual(str, type(usrDict["updated_at"]))

    def test_for_to_dictOutput(self):
        dtime = datetime.today()
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = dtime
        tDict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat(),
        }
        self.assertDictEqual(usr.to_dict(), tDict)

    def test_for_contrast_to_dictDunderDict(self):
        usr = User()
        self.assertNotEqual(usr.to_dict(), usr.__dict__)

    def test_for_to_dict_withArgument(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.to_dict(None)


if __name__ == "__main__":
    unittest.main()
