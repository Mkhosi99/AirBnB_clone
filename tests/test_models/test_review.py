#!/usr/bin/python3
"""Unittest module for the Review Class."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_forInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_for_no_argumentInstantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_for_new_instanceStored_inObj(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_if_id_is_a_publicString(self):
        self.assertEqual(str, type(Review().id))

    def test_if_created_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_if_updated_at_is_a_publicDatetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_if_place_id_is_public_a_classAttr(self):
        rev = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rev))
        self.assertNotIn("place_id", rev.__dict__)

    def test_if_user_id_is_public_a_classAttr(self):
        rev = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rev))
        self.assertNotIn("user_id", rev.__dict__)

    def test_if_text_is_public_a_classAttr(self):
        rev = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rev))
        self.assertNotIn("text", rev.__dict__)

    def test_if_two_reviews_have_uniqueId(self):
        rev1 = Review()
        rev2 = Review()
        self.assertNotEqual(rev1.id, rev2.id)

    def test_if_two_reviews_are_different_for_created_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.created_at, rev2.created_at)

    def test_if_two_reviews_are_different_for_updated_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.updated_at, rev2.updated_at)

    def test_for_string_representation(self):
        dtime = datetime.today()
        dtime_repr = repr(dtime)
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = dtime
        revStr = rev.__str__()
        self.assertIn("[Review] (123456)", revStr)
        self.assertIn("'id': '123456'", revStr)
        self.assertIn("'created_at': " + dtime_repr, revStr)
        self.assertIn("'updated_at': " + dtime_repr, revStr)

    def test_unused_arguments(self):
        rev = Review(None)
        self.assertNotIn(None, rev.__dict__.values())

    def test_for_instantiation_that_have_kwargs(self):
        dtm = datetime.today()
        dtm_iso = dtm.isoformat()
        rev = Review(id="345", created_at=dtm_iso, updated_at=dtm_iso)
        self.assertEqual(rev.id, "345")
        self.assertEqual(rev.created_at, dtm)
        self.assertEqual(rev.updated_at, dtm)

    def test_for_instantiation_with_noKwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_forSave(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        rev = Review()
        sleep(0.05)
        firstUpdate_at = rev.updated_at
        rev.save()
        self.assertLess(firstUpdate_at, rev.updated_at)

    def test_for_twoSaves(self):
        rev = Review()
        sleep(0.05)
        firstUpdate_at = rev.updated_at
        rev.save()
        secondUpdate_at = rev.updated_at
        self.assertLess(firstUpdate_at, secondUpdate_at)
        sleep(0.05)
        rev.save()
        self.assertLess(secondUpdate_at, rev.updated_at)

    def test_for_save_withArgument(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.save(None)

    def test_forSave_and_updates_file(self):
        rev = Review()
        rev.save()
        revId = "Review." + rev.id
        with open("file.json", "r") as f:
            self.assertIn(revId, f.read())


class TestReview_for_toDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_for_to_dictType(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_if_to_dict_has_correctKeys(self):
        rev = Review()
        self.assertIn("id", rev.to_dict())
        self.assertIn("created_at", rev.to_dict())
        self.assertIn("updated_at", rev.to_dict())
        self.assertIn("__class__", rev.to_dict())

    def test_if_to_dict_has_addedAttr(self):
        rev = Review()
        rev.middleName = "Holberton"
        rev.my_number = 98
        self.assertEqual("Holberton", rev.middleName)
        self.assertIn("my_number", rev.to_dict())

    def test_if_to_dict_datetimeAttr_areStrings(self):
        rev = Review()
        revDict = rev.to_dict()
        self.assertEqual(str, type(revDict["id"]))
        self.assertEqual(str, type(revDict["created_at"]))
        self.assertEqual(str, type(revDict["updated_at"]))

    def test_for_to_dictOutput(self):
        dtime = datetime.today()
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = dtime
        tDict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dtime.isoformat(),
            'updated_at': dtime.isoformat(),
        }
        self.assertDictEqual(rev.to_dict(), tDict)

    def test_for_contrast_to_dictDunderDict(self):
        rev = Review()
        self.assertNotEqual(rev.to_dict(), rev.__dict__)

    def test_for_to_dict_withArgument(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.to_dict(None)


if __name__ == "__main__":
    unittest.main()
