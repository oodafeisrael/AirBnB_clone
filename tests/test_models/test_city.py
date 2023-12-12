#!/usr/bin/python3
"""
Defines unittests for models/city.py.
Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        """Test instantiation with no arguments."""
        self.assertEqual(City, type(City()))


    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None as kwargs."""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)


    def test_save_with_arg(self):
        """Test save method with argument."""
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def test_save_updates_file(self):
        """Test if save method updates the file."""
        cy = City()
        cy.save()
        cyid = "City." + cy.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary."""
        self.assertTrue(dict, type(City().to_dict()))


    def test_to_dict_with_arg(self):
        """Test to_dict method with argument."""
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
