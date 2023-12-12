#!/usr/bin/python3
"""
Defines unittests for models/place.py.
Unittest classes:
    TestPlaceInstantiation
    TestPlaceSave
    TestPlaceToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlaceInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        """Test instantiation with no arguments."""
        self.assertEqual(Place, type(Place()))


    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None as kwargs."""
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

    @classmethod
    def setUp(self):
        """Set up test environment."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        pl = Place()
        sleep(0.05)
        first_updated_at = pl.updated_at
        pl.save()
        self.assertLess(first_updated_at, pl.updated_at)


    def test_save_with_arg(self):
        """Test save method with argument."""
        pl = Place()
        with self.assertRaises(TypeError):
            pl.save(None)

    def test_save_updates_file(self):
        """Test if save method updates the file."""
        pl = Place()
        pl.save()
        plid = "Place." + pl.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlaceToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary."""
        self.assertTrue(dict, type(Place().to_dict()))


    def test_to_dict_with_arg(self):
        """Test to_dict method with argument."""
        pl = Place()
        with self.assertRaises(TypeError):
            pl.to_dict(None)


if __name__ == "__main__":
    unittest.main()
