#!/usr/bin/python3
"""
Defines unittests for models/state.py.
Unittest classes:
    TestStateInstantiation
    TestStateSave
    TestStateToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self):
        """Test instantiation with no arguments."""
        self.assertEqual(State, type(State()))


    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None as kwargs."""
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        self.assertLess(first_updated_at, st.updated_at)


    def test_save_with_arg(self):
        """Test save method with argument."""
        st = State()
        with self.assertRaises(TypeError):
            st.save(None)

    def test_save_updates_file(self):
        """Test if save method updates the file."""
        st = State()
        st.save()
        stid = "State." + st.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


class TestStateToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary."""
        st = State()
        self.assertTrue(dict, type(st.to_dict()))


    def test_to_dict_with_arg(self):
        """Test to_dict method with argument."""
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()
