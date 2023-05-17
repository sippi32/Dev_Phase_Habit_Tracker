import unittest
import pytest
from unittest import mock
from unittest.mock import Mock
from unittest.mock import MagicMock, patch
from main import login_screen
from main import database_connection_screen
from database import MySQLDatabase
import database
import main
from datetime import datetime as dt
from datetime import timedelta
import tkinter as tk
from tkinter import ttk

class TestMain(unittest.TestCase):
    @classmethod
    def setUp(self):
        print("\nRunning setUp method..")
        self.db = MySQLDatabase('testhost','root','testpassword')
        self.db.cursor = mock.MagicMock()
        self.db.connection = mock.MagicMock()

    @classmethod
    def tearDown(self):
        print("Running tear down method")

    @mock.patch('main.database_connection_screen.open_next_window')
    @mock.patch('main.mysql.connector.connect')
    @mock.patch('main.MySQLDatabase')
    def test_confirm_values(self, mock_MySQLDatabase, mock_connect, mock_open_next_window):
        print(" Running test_confirm_values")
    
        # create a database_connection_screen object
        db_screen = database_connection_screen()

        # create mock Entry widgets
        db_screen.entry_host = Mock()
        db_screen.entry_user = Mock()
        db_screen.entry_port = Mock()
        db_screen.entry_password = Mock()
        db_screen.entry_database = Mock()

        # configure mock Entry widgets to return desired values when get() is called
        db_screen.entry_host.get.return_value = 'testhost'
        db_screen.entry_user.get.return_value = 'testuser'
        db_screen.entry_port.get.return_value = 3306
        db_screen.entry_password.get.return_value = 'testpass'
        db_screen.entry_database.get.return_value = 'testdb'

        mock_db_instance = mock_MySQLDatabase.return_value
        mock_connect.return_value = mock.MagicMock()

        # Call the confirm_values function
        db_screen.confirm_values()

        # assert that the database connection was created successfully
        mock_MySQLDatabase.assert_called_once_with('testhost', 'testuser', 'testpass', 3306 )
        mock_db_instance.create_database.assert_called_once_with('testdb')
        mock_connect.assert_called_once_with(host='testhost', user='testuser',port=3306, password='testpass', database='testdb')
        mock_open_next_window.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    @mock.patch.object(MySQLDatabase, 'insert_data') 
    @mock.patch.object(login_screen, 'register')
    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch('tkinter.Toplevel') 
    def test_save_registration_correct_entries(self, mock_toplevel, mock_show_info, mock_connect, mock_disconnect, mock_insert_data, mock_register):
        print(" Running test_save_registration_correct_entries")

        # patch the Toplevel class so that it doesn't create an actual popup window
        with patch('tkinter.Toplevel') as MockPopup:
            mock_popup_instance = mock_toplevel.return_value
            log_screen = login_screen()
            log_screen.popup = mock_popup_instance

        # create mock entry widgets and return values
        log_screen.entry_first_name = MagicMock()
        log_screen.entry_first_name.get.return_value = "Marc"
        log_screen.entry_last_name = MagicMock()
        log_screen.entry_last_name.get.return_value = "Fischer"
        log_screen.entry_username = MagicMock()
        log_screen.entry_username.get.return_value = "MAFI"
        log_screen.entry_password = MagicMock()
        log_screen.entry_password.get.return_value = "password123"
        log_screen.entry_email = MagicMock()
        log_screen.entry_email.get.return_value = "mafi@example.com"
        log_screen.entry_phone_number = MagicMock()
        log_screen.entry_phone_number.get.return_value = "1234567890"

        expected_data = {'username': 'MAFI', 'first_name': "Marc", 'last_name': 'Fischer', 'username': 'MAFI', 'password': 'password123', 'email': 'mafi@example.com', 'phone_number': '1234567890', 'created_time': dt.now(), 'last_update': dt.now() }

        log_screen.save_registration()

        # Asserts
        self.db.insert_data.assert_called_once_with("user_table",expected_data)
        mock_show_info.assert_called_once_with("Success", "User: MAFI successfully registered")
        mock_popup_instance.destroy.assert_called_once()
    


if __name__ == '__main__':
    unittest.main()
    





















# def test_save_registration():
#     with patch.object(login_screen, 'db'), \
#          patch.object(login_screen, 'popup', MagicMock()), \
#          patch.object(login_screen, 'entry_first_name'), \
#          patch.object(login_screen, 'entry_last_name'), \
#          patch.object(login_screen, 'entry_username'), \
#          patch.object(login_screen, 'entry_password'), \
#          patch.object(login_screen, 'entry_email'), \
#          patch.object(login_screen, 'entry_phone_number'):
    
#         # Mock the Entry.get method for each Entry object
#         login_screen.entry_first_name.get.return_value = "John"
#         login_screen.entry_last_name.get.return_value = "Doe"
#         login_screen.entry_username.get.return_value = "johndoe"
#         login_screen.entry_password.get.return_value = "password"
#         login_screen.entry_email.get.return_value = "johndoe@example.com"
#         login_screen.entry_phone_number.get.return_value = "1234567890"
        
#         # Create the login_screen object
#         login_screen_obj = login_screen()
        
#         # Call the save_registration method
#         login_screen_obj.save_registration()
        
#         # Assert that the insert_data method was called with the correct arguments
#         login_screen_obj.db.insert_data.assert_called_with("user_table", {
#             'username': 'johndoe',
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'password': 'password',
#             'email': 'johndoe@example.com',
#             'phone_number': '1234567890',
#             'created_time': login_screen_obj.created_time,
#             'last_update': login_screen_obj.last_update
#         })