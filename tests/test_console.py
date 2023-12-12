#!/usr/bin/python3
"""Module for TestHBNBCommand class."""


import console
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage
import datetime
import sys
import re
import os


class TestHBNBCommand(unittest.TestCase):
    """
    Test class for HBNBCommand class
    """

    def setUp(self):
        """
        Set up test environment
        """
        self.console = HBNBCommand()

    def tearDown(self):
        """
        Clean up after test
        """
        pass

    def capture_output(self, func, *args):
        """
        Capture console output for testing
        """
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            func(*args)
            return captured_output.getvalue().strip()
        finally:
            sys.stdout = sys.__stdout__

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_create(self):
        """
        Test create command
        """
        for class_name in ['BaseModel', 'User',
                           'State', 'City', 'Place', 'Amenity', 'Review']:
            command = f"create {class_name}"
            output = self.capture_output(self.console.onecmd, command)
            self.assertTrue(len(output) == 36)  # Check for ID

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_show(self):
        """
        Test show command
        """
        for class_name in ['BaseModel', 'User',
                           'State', 'City', 'Place', 'Amenity', 'Review']:
            create_command = f"create {class_name}"
            obj_id = self.capture_output(self.console.onecmd,
                                         create_command).strip()

            show_command = f"show {class_name} {obj_id}"
            output = self.capture_output(self.console.onecmd, show_command)
            self.assertTrue(obj_id in output)

            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                show_command = f"show {class_name} {obj_id}"
                self.console.onecmd(show_command)
                output = mock_stdout.getvalue().strip()
                self.assertTrue(obj_id in output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_destroy(self):
        """
        Test destroy command
        """
        for class_name in ['BaseModel', 'User',
                           'State', 'City', 'Place', 'Amenity', 'Review']:
            create_command = f"create {class_name}"
            obj_id = self.capture_output(self.console.onecmd,
                                         create_command).strip()

            destroy_command = f"destroy {class_name} {obj_id}"
            output = self.capture_output(self.console.onecmd, destroy_command)
            self.assertEqual(output, '')

            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                destroy_command = f"destroy {class_name} {obj_id}"
                self.console.onecmd(destroy_command)
                output = mock_stdout.getvalue().strip()
                self.assertEqual(output, '')

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_all(self):
        """
        Test all command
        """
        for class_name in ['BaseModel', 'User',
                           'State', 'City', 'Place', 'Amenity', 'Review']:
            create_command = f"create {class_name}"
            self.capture_output(self.console.onecmd, create_command)

        all_command = "all"
        output = self.capture_output(self.console.onecmd, all_command)
        self.assertTrue(all(class_name in output for class_name in
                            ['BaseModel',
                             'User', 'State',
                             'City', 'Place',
                             'Amenity', 'Review']))

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            all_command = "all"
            self.console.onecmd(all_command)
            output = mock_stdout.getvalue().strip()
            self.assertTrue(all(class_name in output for class_name in
                                ['BaseModel',
                                 'User', 'State', 'City',
                                 'Place', 'Amenity',
                                 'Review']))

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_count(self):
        """
        Test count command
        """
        for class_name in ['BaseModel', 'User',
                           'State', 'City', 'Place', 'Amenity',
                           'Review']:
            create_command = f"create {class_name}"
            self.capture_output(self.console.onecmd, create_command)

        count_command = "count"
        output = self.capture_output(self.console.onecmd, count_command)
        self.assertTrue(all(class_name in output for class_name in
                            ['BaseModel',
                             'User', 'State',
                             'City', 'Place', 'Amenity',
                             'Review']))

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            count_command = "count"
            self.console.onecmd(count_command)
            output = mock_stdout.getvalue().strip()
            self.assertTrue(all(class_name in output for class_name in
                                ['BaseModel',
                                 'User', 'State',
                                 'City', 'Place',
                                 'Amenity', 'Review']))

    @patch('sys.stdout', new_callable=StringIO)
    def test_do_update(self):
        """
        Test update command
        """
        for class_name in ['BaseModel',
                           'User', 'State',
                           'City', 'Place', 'Amenity',
                           'Review']:
            create_command = f"create {class_name}"
            obj_id = self.capture_output(self.console.onecmd,
                                         create_command).strip()

            update_command = f"update {class_name} {obj_id} name 'New Name'"
            output = self.capture_output(self.console.onecmd, update_command)
            self.assertEqual(output, '')

            show_command = f"show {class_name} {obj_id}"
            output = self.capture_output(self.console.onecmd, show_command)
            self.assertTrue('New Name' in output)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            update_command = f"update {class_name} {obj_id} name 'New Name'"
            self.console.onecmd(update_command)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '')


if __name__ == '__main__':
    unittest.main()
