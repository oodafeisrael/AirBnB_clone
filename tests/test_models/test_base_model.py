#!/usr/bin/python3
"""
Defines unittests for models/base_model.py.
Unittest classes:
    TestBaseModelInstantiation
    TestBaseModelSave
    TestBaseModelToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        """Test instantiation with no arguments."""
        self.assertEqual(BaseModel, type(BaseModel()))


    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None as kwargs."""
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        """Test instantiation with both args and kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)


class TestBaseModelSave(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        """Set up test environment."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """Clean up after test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Test single save method call."""
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)


    def test_save_with_arg(self):
        """Test save method with argument."""
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_updates_file(self):
        """Test if save method updates the file."""
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestBaseModelToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary."""
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))


    def test_to_dict_with_arg(self):
        """Test to_dict method with argument."""
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
