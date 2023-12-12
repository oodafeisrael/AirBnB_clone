#!/usr/bin/python3
"""
Defines unittests for models/review.py.
Unittest classes:
    TestReviewInstantiation
    TestReviewSave
    TestReviewToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReviewInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        """Test instantiation with no arguments."""
        self.assertEqual(Review, type(Review()))


    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None as kwargs."""
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewSave(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        self.assertLess(first_updated_at, rv.updated_at)


    def test_save_with_arg(self):
        """Test save method with argument."""
        rv = Review()
        with self.assertRaises(TypeError):
            rv.save(None)

    def test_save_updates_file(self):
        """Test if save method updates the file."""
        rv = Review()
        rv.save()
        rvid = "Review." + rv.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReviewToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary."""
        rv = Review()
        self.assertTrue(dict, type(rv.to_dict()))


    def test_to_dict_with_arg(self):
        """Test to_dict method with argument."""
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
