#!/usr/bin/python3
"""Defines unittests for the HBNBCommand console."""
import os
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage

class TestHBNBCommand(unittest.TestCase):
    """Unittests for the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """Setup for HBNBCommand tests.

        Temporarily rename any existing file.json.
        Reset FileStorage objects dictionary.
        Create an instance of the command interpreter.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        # Create an instance of the HBNBCommand class.
        cls.console = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Teardown for HBNBCommand tests.

        Restore the original file.json.
        Delete the test HBNBCommand instance.
        """
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.console

    def setUp(self):
        """Reset FileStorage objects dictionary."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Remove any created file.json."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_create_errors(self):
        """Test errors in the create command."""
        # Test for missing class name
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **\n", output.getvalue())
        # Test for non-existent class
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create NonExistentClass")
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_create_command(self):
        """Test the create command for various classes."""
        # Create BaseModel instance
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create BaseModel")
            bm_id = output.getvalue().strip()

        # Create User instance
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create User")
            user_id = output.getvalue().strip()

        # Create State instance
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create State")
            state_id = output.getvalue().strip()

        # Create Place instance
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create Place")
            place_id = output.getvalue().strip()

        # Create City instance
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create City")
            city_id = output.getvalue().strip()

        # Create Review instance
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create Review")
            review_id = output.getvalue().strip()

        # Create Amenity instance
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("create Amenity")
            amenity_id = output.getvalue().strip()

        # Verify created instances with "all" command
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("all BaseModel")
            self.assertIn(bm_id, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("all User")
            self.assertIn(user_id, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("all State")
            self.assertIn(state_id, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("all Place")
            self.assertIn(place_id, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("all City")
            self.assertIn(city_id, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("all Review")
            self.assertIn(review_id, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("all Amenity")
            self.assertIn(amenity_id, output.getvalue())

    def test_create_with_kwargs(self):
        """Test the create command with keyword arguments."""
        # Create Place instance with kwargs
        with patch("sys.stdout", new=StringIO()) as output:
            command = 'create Place city_id="0001" name="My_house" number_rooms=4 latitude=37.77 longitude=43.434'
            self.console.onecmd(command)
            place_id = output.getvalue().strip()

        # Verify created instance and its attributes
        with patch("sys.stdout", new=StringIO()) as output:
            self.console.onecmd("all Place")
            output_str = output.getvalue()
            self.assertIn(place_id, output_str)
            self.assertIn("'city_id': '0001'", output_str)
            self.assertIn("'name': 'My house'", output_str)
            self.assertIn("'number_rooms': 4", output_str)
            self.assertIn("'latitude': 37.77", output_str)
            self.assertIn("'longitude': 43.434", output_str)


if __name__ == "__main__":
    unittest.main()
