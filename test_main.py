import unittest
import pytest
from unittest import mock
from unittest.mock import Mock
from unittest.mock import MagicMock, patch
from main import login_screen
from main import database_connection_screen
from main import main_screen
from database import MySQLDatabase
import database
import main
from datetime import datetime as dt
from datetime import timedelta
import tkinter as tk

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
        db_screen.entry_password = Mock()
        db_screen.entry_database = Mock()

        # configure mock Entry widgets to return desired values when get() is called
        db_screen.entry_host.get.return_value = 'testhost'
        db_screen.entry_user.get.return_value = 'testuser'
        db_screen.entry_password.get.return_value = 'testpass'
        db_screen.entry_database.get.return_value = 'testdb'

        mock_db_instance = mock_MySQLDatabase.return_value
        mock_connect.return_value = mock.MagicMock()

        # Call the confirm_values function
        db_screen.confirm_values()

        # assert that the database connection was created successfully
        mock_MySQLDatabase.assert_called_once_with('testhost', 'testuser', 'testpass')
        mock_db_instance.create_database.assert_called_once_with('testdb')
        mock_connect.assert_called_once_with(host='testhost', user='testuser', password='testpass', database='testdb')
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

    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch.object(MySQLDatabase, 'check_value')
    @mock.patch.object(MySQLDatabase, 'get_streak')
    @mock.patch.object(MySQLDatabase, 'get_active_habit_ID')
    @mock.patch.object(MySQLDatabase, 'get_habit_ID')
    @mock.patch.object(MySQLDatabase, 'update_data')
    @patch('os.getenv', side_effect=['db_name,db_user,db_pass,db_host', 'my_username,my_password'])
    @patch.object(MySQLDatabase, 'get_userID', return_value=100)
    @mock.patch('tkinter.Toplevel')
    def test_check_habit_successfull_checkoff_zero_streak(self, mock_toplevel, mock_get_userID, mock_getenv, mock_update_data, mock_get_habit_ID, mock_get_active_habit_ID, mock_get_streak, mock_check_value, mock_showinfo):
        print(" Running test_check_habit_successfull_checkoff")

        # Set up mock database responses
        mock_get_habit_ID.return_value = [1]
        print(mock_get_habit_ID)
        mock_get_active_habit_ID.return_value = 1
        print(mock_get_active_habit_ID)
        mock_get_streak.return_value = 0
        print(mock_get_streak)
        mock_check_value.side_effect = [[dt.now()], [dt.now() + timedelta(days=1)]]
        print(mock_check_value)
 
        # patch the Toplevel class so that it doesn't create an actual popup window
        with patch('tkinter.Toplevel') as MockPopup:
            mock_popup_instance = mock_toplevel.return_value
            main_screen_instance = main_screen()



        expected_selection = {"values": ["test-habit", "description", "daily"]}

        # patch the active_habits_tree.selection() method to return the expected selection
        with patch.object(main_screen_instance.active_habits_tree, "selection", return_value=expected_selection):
            # call the check_habit method
            main_screen_instance.check_habit()

        # Set up the mock for the active_habits_tree attribute

        # main_screen_instance.active_habits_tree = MagicMock()

        expected_data = {"streak": 1, "last_check": dt.now(), "update_expiry": mock_check_value }

        # Set up the mock for the item method of the active_habits_tree
        #main_screen_instance.active_habits_tree.item.return_value = {"values": ["test-habit", "description", "daily"]}

        # Call the check_habit method and assert that the new_streak is 1
        #new_streak = main_screen_instance.new_streak
        

        #main_screen_instance.check_habit()

        # Check that the mocked environment variables were retrieved and the user ID was set correctly
        # assert mock_getenv.call_count == 2
        # assert main_screen_instance.username == 'my_username'
        # assert main_screen_instance.password == 'my_password'
        # assert main_screen_instance.user_ID == 100
        # assert new_streak == 1
        mock_update_data.assert_called_once_with("active_user_habits", expected_data, "active_habits", 1)

    







    
    # @mock.patch('os.getenv')
    # @mock.patch.object(MySQLDatabase, 'get_userID', return_value=123)
    # @mock.patch.object(MySQLDatabase, 'check_value')
    # @mock.patch.object(MySQLDatabase, 'get_streak', return_value=0)
    # @mock.patch.object(MySQLDatabase, 'get_active_habit_ID', return_value="1")
    # @mock.patch.object(MySQLDatabase, 'get_habit_ID', return_value="1")
    # @mock.patch.object(MySQLDatabase, 'update_data')
    # @mock.patch.object(main_screen, '__init__')
    # def test_check_habit_successfull_checkoff_zero_streak(self, mock_main_screen, mock_update_data, mock_get_habit_ID, mock_get_active_habit_ID, mock_get_streak, mock_check_value, mock_get_user_ID, mock_getenv):
    #     print(" Running test_check_habit_successfull_checkoff")

    #     # Set up the mocked environment variables
    #     mock_getenv.side_effect = lambda x: {
    #     "Database_Variables": "db_name, db_user, db_pass, db_host",
    #     "User_Variables": "my_username, my_password"
    #     }.get(x)

    #     # # Create a mocked main_screen object
    #     # with mock.patch.object(main_screen, '__init__', return_value=None):
    #     #     main_screen_object = main_screen()

    #     # Create a mocked main_screen object
    #     main_screen_object = mock_main_screen.return_value
    #     active_habits_tree = MagicMock()
    #     main_screen_object.active_habits_tree = active_habits_tree

    #    # Create a mock object for the active_habits_tree
    #     active_habits_tree = MagicMock()
        
    #     # Set the return value of the selection method
    #     active_habits_tree.selection.return_value = ["test_habit", 0, "daily"]

    #     mock_check_value.return_value = dt.now() + timedelta(hours=5)
    #     update_expiry = mock_check_value()

    

    #     # Expected data for update_data function in database

    #     expected_data = {"streak": 1, "last_check": dt.now(), "update_expiry": update_expiry + timedelta(days=1) }


    #     main_screen_object.check_habit()

    #     mock_update_data.assert_called_once_with("active_user_habits", expected_data, "active_habits", 1)
    


 

        









    # @mock.patch.object(MySQLDatabase, 'get_userID')
    # @mock.patch('main.login_screen.open_main_screen')
    # @mock.patch('main.os.environ')
    # @mock.patch.object(MySQLDatabase, 'disconnect')
    # @mock.patch('tkinter.messagebox.showinfo')
    # @mock.patch.object(MySQLDatabase, 'connect')
    # @mock.patch('tkinter.Toplevel') 
    # def test_login_process_successfull(self, mock_toplevel, mock_connect, mock_show_info, mock_disconnect, mock_os, mock_open_main_screen, mock_get_userID):
    #     print(" Running test_login_successfull")


    #     # patch the Toplevel class so that it doesn't create an actual popup window
    #     with patch('tkinter.Toplevel') as MockPopup:
    #         mock_popup_instance = mock_toplevel.return_value
    #         log_screen = login_screen()
    #         log_screen.popup = mock_popup_instance
        
    #     # create mock objects
    #     # mock_cursor = Mock()
    #     # self.db.return_value.cursor.return_value = mock_cursor
    #     mock_get_userID.return_value = 1
    #     log_screen.entry_username = MagicMock()
    #     log_screen.entry_username.get.return_value = "Test_user"
    #     log_screen.entry_password = MagicMock()
    #     log_screen.entry_password.get.return_value = "test_password"
        

    #     expected_query = "SELECT * FROM user_table WHERE username = %s AND password = %s"

    #     # Mock the database cursor's fetchall() method to return an empty list
    #     self.db.cursor.fetchone.return_value = ['user_1',]

    #     # Execute the login_process function
    #     log_screen.login_process()


    #     # Asserts
    #     mock_connect.assert_called_once()
    #     self.db.cursor.execute.assert_called_once_with(expected_query,("Test_user", "test_password"))
    #     mock_os.__setitem__.assert_called_once_with('User_Variables', 'test_user,test_password')
    #     mock_os.__setitem__.assert_called_once_with('active_user_ID', '1')
    #     mock_show_info.assert_called_once_with("Success", "Hello Test_user you can now enjoy the Habit Tracker! Have fun and stay active!")
    #     mock_disconnect.assert_called_once()
    #     mock_popup_instance.destroy.assert_called_once()
    #     mock_open_main_screen.assert_called_once()






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