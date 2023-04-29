import unittest
from unittest.mock import patch, Mock
import os
from main import login_screen
from database import MySQLDatabase

class TestLoginScreen(unittest.TestCase):
    def setUp(self):
        # Patch the os.getenv function call to return the expected string
        self.getenv_patcher = patch('os.getenv', return_value="host,user,password,database")
        self.getenv_patcher.start()
        self.login_screen = login_screen()
        
    def test_save_registration_success(self):
        mock_db = Mock()
        self.login_screen.db = mock_db
        # Set up the GUI with valid user data
        self.login_screen.entry_first_name.insert(0, "Marc")
        self.login_screen.entry_last_name.insert(0, "Fischer")
        self.login_screen.entry_username.insert(0, "Marc")
        self.login_screen.entry_password.insert(0, "password")
        self.login_screen.entry_email.insert(0, "marc@example.com")
        self.login_screen.entry_phone_number.insert(0, "1234567890")

        self.login_screen.save_registration()

        expected_data = {'username': 'Marc', 'first_name': 'Marc', 'last_name': 'Fischer', 'password': 'password', 'email': 'marc@example.com', 'phone_number': '1234567890', 'created_time': Mock.ANY, 'last_update': Mock.ANY}
        mock_db.insert_data.assert_called_once_with("user_table", expected_data)

        self.login_screen.popup.destroy.assert_called_once()
       
    def test_save_registration_missing_fields(self):
        # Set up the GUI with missing fields
        self.login_screen.entry_first_name.insert(0, "Marc")
        self.login_screen.entry_last_name.insert(0, "Fischer")
        self.login_screen.entry_username.insert(0, "marc")
        self.login_screen.entry_email.insert(0, "marc@example.com")
        self.login_screen.entry_phone_number.insert(0, "1234567890")
        
        # Call the function and check if the error message is shown
        with patch.object(self.login_screen, 'db') as mock_db:
            self.login_screen.save_registration()
        self.assertIn("Please fill in all fields", self.login_screen.popup.showerror.call_args[0][1])
        self.login_screen.popup.destroy.assert_not_called()
        
    def test_save_registration_invalid_phone_number(self):
        # Set up the GUI with an invalid phone number
        self.login_screen.entry_first_name.insert(0, "Marc")
        self.login_screen.entry_last_name.insert(0, "Fischer")
        self.login_screen.entry_username.insert(0, "Marc")
        self.login_screen.entry_password.insert(0, "password")
        self.login_screen.entry_email.insert(0, "marc@example.com")
        self.login_screen.entry_phone_number.insert(0, "12345abcde")
        
        # Call the function and check if the error message is shown
        with patch.object(self.login_screen, 'db') as mock_db:
            self.login_screen.save_registration()
        self.assertIn("Phone number must contain only digits", self.login_screen.popup.showerror.call_args[0][1])
        self.login_screen.popup.destroy.assert_not_called()