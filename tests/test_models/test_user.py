#!/usr/bin/python3
"""
Defines unittests for models/user.py.
Unittest classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_no_args_instantiates(self):
        """Test instantiation with no arguments."""
        self.assertEqual(User, type(User()))


    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None as kwargs."""
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Unittests for testing save method of the User class."""

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
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)


    def test_save_with_arg(self):
        """Test save method with argument."""
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def test_save_updates_file(self):
        """Test if save method updates the file."""
        us = User()
        us.save()
        usid = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUserToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary."""
        self.assertTrue(dict, type(User().to_dict()))


    def test_to_dict_with_arg(self):
        """Test to_dict method with argument."""
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
