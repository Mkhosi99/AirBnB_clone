#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_create_new_instant(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_with_no_arguments(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_an_argument(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_a_private_string(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_obj_is_a_private_dictionary(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_if_it_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_with_file_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def prepare(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def cleanUp(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_for_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_an_argument(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_for_new(self):
        bsm = BaseModel()
        usr = User()
        sta = State()
        plc = Place()
        cty = City()
        amnty = Amenity()
        rev = Review()
        models.storage.new(bsm)
        models.storage.new(usr)
        models.storage.new(sta)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amnty)
        models.storage.new(rev)
        self.assertIn("BaseModel." + bsm.id, models.storage.all().keys())
        self.assertIn(bsm, models.storage.all().values())
        self.assertIn("User." + usr.id, models.storage.all().keys())
        self.assertIn(usr, models.storage.all().values())
        self.assertIn("State." + sta.id, models.storage.all().keys())
        self.assertIn(sta, models.storage.all().values())
        self.assertIn("Place." + plc.id, models.storage.all().keys())
        self.assertIn(plc, models.storage.all().values())
        self.assertIn("City." + cty.id, models.storage.all().keys())
        self.assertIn(cty, models.storage.all().values())
        self.assertIn("Amenity." + amnty.id, models.storage.all().keys())
        self.assertIn(amnty, models.storage.all().values())
        self.assertIn("Review." + rev.id, models.storage.all().keys())
        self.assertIn(rev, models.storage.all().values())

    def test_new_with_an_argument(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None_added(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_for_save(self):
        bsm = BaseModel()
        usr = User()
        sta = State()
        plc = Place()
        cty = City()
        amnty = Amenity()
        rev = Review()
        models.storage.new(bsm)
        models.storage.new(usr)
        models.storage.new(sta)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amnty)
        models.storage.new(rev)
        models.storage.save()
        saveText = ""
        with open("file.json", "r") as f:
            saveText = f.read()
            self.assertIn("BaseModel." + bsm.id, saveText)
            self.assertIn("User." + usr.id, saveText)
            self.assertIn("State." + sta.id, saveText)
            self.assertIn("Place." + plc.id, saveText)
            self.assertIn("City." + cty.id, saveText)
            self.assertIn("Amenity." + amnty.id, saveText)
            self.assertIn("Review." + rev.id, saveText)

    def test_save_with_an_argument(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_for_reload(self):
        bsm = BaseModel()
        usr = User()
        sta = State()
        plc = Place()
        cty = City()
        amnty = Amenity()
        rev = Review()
        models.storage.new(bsm)
        models.storage.new(usr)
        models.storage.new(sta)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amnty)
        models.storage.new(rev)
        models.storage.save()
        models.storage.reload()
        objcts = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bsm.id, objcts)
        self.assertIn("User." + usr.id, objcts)
        self.assertIn("State." + sta.id, objcts)
        self.assertIn("Place." + plc.id, objcts)
        self.assertIn("City." + cty.id, objcts)
        self.assertIn("Amenity." + amnty.id, objcts)
        self.assertIn("Review." + rev.id, objcts)

    def test_reload_with_an_argument(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
