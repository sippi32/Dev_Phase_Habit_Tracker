from database import MySQLDatabase
from main import main_screen
import unittest
import datetime
from datetime import datetime as dt
from datetime import timedelta
from unittest import mock
import os


class TestMainScreen(unittest.TestCase):
    @classmethod
    @mock.patch.object(main_screen, '__init__')
    @mock.patch.dict(os.environ, {"Database_Variables": "mock_value1,mock_value2,mock_value3,mock_value4"})
    @mock.patch.dict(os.environ, {"User_Variables": "mock_value1,mock_value2,mock_value3,mock_value4"})
    def setUp(cls, mock___init__, *args, **kwargs):
        print("\nRunning setUp method..")
        cls.db = MySQLDatabase('localhost','root','password')
        cls.db.cursor = mock.MagicMock()
        cls.db.connection = mock.MagicMock()
        cls.mock_screen = main_screen()
        cls.mock_screen.message_box = mock.MagicMock()
        # with mock.patch("main.main_screen") as mock_main_screen:
        #     cls.mock_screen = mock_main_screen.return_value
        #     cls.mock_screen.message_box = mock.MagicMock()
    
    @classmethod
    def tearDown(cls):
        print("Running tear down method")


    @mock.patch('database.MySQLDatabase.get_habit_ID')
    @mock.patch('database.MySQLDatabase.get_active_habit_ID')
    @mock.patch('database.MySQLDatabase.get_streak')
    @mock.patch('database.MySQLDatabase.check_value')
    def test_check_habit_daily_streak_0(self, mock_get_habit_ID, mock_get_active_habit_ID, mock_get_streak, mock_check_value):
        """
        Test case for the `check_habit` function with interval = "daily" and streak = 0.
        """
        
        # mock_screen = Mock(spec=main_screen)
        # object = mock_screen()
        # Create a mock for the message box
        message_box_mock = mock.MagicMock()
   
        # Set up test input data
        active_habit_name = "Test_habit"
        user_ID = 1
        interval_ID = "daily"
        update_expiry = dt.now() + timedelta(hours = 10)
        new_streak = 0
        data = {}
        expected_new_update_expiry = update_expiry + timedelta(days=1)
        expected_new_streak = 1
        expected_data = {"streak": 1, "last_check": dt.now(), "update_expiry": expected_new_update_expiry}
        mock_get_habit_ID.return_value = 2
        mock_get_active_habit_ID.return_value = 10
        mock_get_streak.return_value = 0
        mock_check_value.return_value = [(f"{update_expiry}",)]

        # Call the check_habit function from the main_screen class
        self.mock_screen.check_habit()

        # Assert that the new_streak is updated and the message box is shown with the correct message
        self.assertEqual(data, expected_data)
        self.assertEqual(new_streak, expected_new_streak)
        self.db.update_data.assert_called_once_with("active_user_habits", data, "active_habits", 1)
        message_box_mock.showinfo.assert_called_once_with("Success", f"Congrats! You have checked you daily habit and you streak continoues. Your next check is available in {timedelta(days=1)}. Stay focused!")


    if __name__ == '__main__':
        unittest.main()


    #@mock.patch('main.main_screen.__init__')

        # Assert that the mock database methods were called correctly
        #self.db.get_habit_ID.assert_called_once_with(1, "Test_habit")
        #self.db.get_active_habit_ID.assert_called_once_with(1, 2, "in progress")
        #self.db.get_streak.assert_called_once_with(10)
        #self.db.check_value.assert_called_with("last_check", "active_user_habits", "active_habits_ID", 10)
