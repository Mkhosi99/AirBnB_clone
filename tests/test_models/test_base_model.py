#!/usr/bin/python3
"""Defines unittests for models/base_model.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_for_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_for_no_arguments_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_for_new_instance_storedIn_obj(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_if_id_is_a_publicString(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_if_created_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_if_updated_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_for_two_models_uniqueId(self):
        bsm1 = BaseModel()
        bsm2 = BaseModel()
        self.assertNotEqual(bsm1.id, bsm2.id)

    def test_for_two_models_if_different_for_created_at(self):
        bsm1 = BaseModel()
        sleep(0.05)
        bsm2 = BaseModel()
        self.assertLess(bsm1.created_at, bsm2.created_at)

    def test_for_two_models_if_different_for_updated_at(self):
        bsm1 = BaseModel()
        sleep(0.05)
        bsm2 = BaseModel()
        self.assertLess(bsm1.updated_at, bsm2.updated_at)

    def test_for_string_representation(self):
        dtime = datetime.today()
        dtime_repr = repr(dtime)
        bsm = BaseModel()
        bsm.id = "123456"
        bsm.created_at = bsm.updated_at = dtime
        bsmStrng = bsm.__str__()
        self.assertIn("[BaseModel] (123456)", bsmStrng)
        self.assertIn("'id': '123456'", bsmStrng)
        self.assertIn("'created_at': " + dtime_repr, bsmStrng)
        self.assertIn("'updated_at': " + dtime_repr, bsmStrng)

    def test_for_unused_arguments(self):
        bsm = BaseModel(None)
        self.assertNotIn(None, bsm.__dict__.values())

    def test_for_instantiation_containing_kwargs(self):
        dtime = datetime.today()
        dtime_iso = dtime.isoformat()
        bsm = BaseModel(id="345", created_at=dtime_iso, updated_at=dtime_iso)
        self.assertEqual(bsm.id, "345")
        self.assertEqual(bsm.created_at, dtime)
        self.assertEqual(bsm.updated_at, dtime)

    def test_for_instantiation_containing_No_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_for_instantiation_containing_args_and_kwargs(self):
        dtm = datetime.today()
        dtm_iso = dtm.isoformat()
        bsm = BaseModel("12", id="345", created_at=dtm_iso, updated_at=dtm_iso)
        self.assertEqual(bsm.id, "345")
        self.assertEqual(bsm.created_at, dtm)
        self.assertEqual(bsm.updated_at, dtm)


class TestBaseModel_for_saving(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def prepare(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def cleanUP(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_for_oneSave(self):
        bsm = BaseModel()
        sleep(0.05)
        firstUpdated_at = bsm.updated_at
        bsm.save()
        self.assertLess(firstUpdated_at, bsm.updated_at)

    def test_for_twoSaves(self):
        bsm = BaseModel()
        sleep(0.05)
        firstUpdated_at = bsm.updated_at
        bsm.save()
        secondUpdated_at = bsm.updated_at
        self.assertLess(firstUpdated_at, secondUpdated_at)
        sleep(0.05)
        bsm.save()
        self.assertLess(secondUpdated_at, bsm.updated_at)

    def test_for_save_with_argument(self):
        bsm = BaseModel()
        with self.assertRaises(TypeError):
            bsm.save(None)

    def test_save_updates_forFile(self):
        bsm = BaseModel()
        bsm.save()
        bsmId = "BaseModel." + bsm.id
        with open("file.json", "r") as f:
            self.assertIn(bsmId, f.read())


class TestBaseModel_for_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dictType(self):
        bsm = BaseModel()
        self.assertTrue(dict, type(bsm.to_dict()))

    def test_to_dict_if_it_has_correct_keys(self):
        bsm = BaseModel()
        self.assertIn("id", bsm.to_dict())
        self.assertIn("created_at", bsm.to_dict())
        self.assertIn("updated_at", bsm.to_dict())
        self.assertIn("__class__", bsm.to_dict())

    def test_to_dict_has_added_attrs(self):
        bsm = BaseModel()
        bsm.name = "Holberton"
        bsm.my_number = 98
        self.assertIn("name", bsm.to_dict())
        self.assertIn("my_number", bsm.to_dict())

    def test_to_dict_if_datetime_attrs_are_strings(self):
        bsm = BaseModel()
        bsmDict = bsm.to_dict()
        self.assertEqual(str, type(bsmDict["created_at"]))
        self.assertEqual(str, type(bsmDict["updated_at"]))

    def test_for_to_dict_output(self):
        dtime = datetime.today()
        bsm = BaseModel()
        bsm.id = "123456"
        bsm.created_at = bsm.updated_at = dtime
        tDict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat()
        }
        self.assertDictEqual(bsm.to_dict(), tDict)

    def test_contrast_to_dict_dunderDict(self):
        bsm = BaseModel()
        self.assertNotEqual(bsm.to_dict(), bsm.__dict__)

    def test_to_dict_with_argument(self):
        bsm = BaseModel()
        with self.assertRaises(TypeError):
            bsm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
