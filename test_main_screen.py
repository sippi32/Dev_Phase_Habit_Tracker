import unittest
from unittest import mock
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
from main import Main_screen
from database import MySQLDatabase
from datetime import timedelta
import datetime 
import tkinter as tk
from tkinter import ttk
from habit import Habit
from category import Category

class TestMain(unittest.TestCase):
    def setUp(self):
        print("\nRunning setUp method..")
        self.db = MySQLDatabase('localhost','root','test')
        self.db.cursor = mock.MagicMock()
        self.db.connection = mock.MagicMock()


    def tearDown(self):
        print("Running tear down method")

    @mock.patch.object(Habit,'create_dict')
    @mock.patch.object(MySQLDatabase,'insert_data')
    @mock.patch.object(MySQLDatabase,'get_category_ID')
    @mock.patch.object(MySQLDatabase,'get_habit_ID')
    @mock.patch('tkinter.messagebox.showerror')
    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch('tkinter.Tk') 
    def test_save_habit_one_added(self, mock_tk, mock_showinfo, mock_showerror, mock_get_habit_ID, mock_get_category_ID, mock_insert_data, mock_create_dict):
        print(" Running test_save_habit_one_added")
        
        mock_popup_instance = mock_tk.return_value
        mock_main_screen = Main_screen(isTest=True)
        mock_main_screen.db = self.db
        mock_main_screen.popup = mock_popup_instance
        mock_main_screen.user_ID = 1        

        # create mock Entry widgets
        mock_main_screen.entry_habit_name = Mock()
        mock_main_screen.entry_description = Mock()
        mock_main_screen.category_var = Mock()
        
        # configure mock Entry widgets to return desired values when get() is called
        mock_main_screen.entry_habit_name.get.return_value = 'new_test_habit'
        mock_main_screen.entry_description.get.return_value = 'A test habit'
        mock_main_screen.category_var.get.return_value = 'Test category'

        mock_creation_date = '2023-05-17T00:00:00.00000'

        mock_main_screen.category_ID = 1
        mock_get_category_ID.return_value = 1
        mock_get_habit_ID.return_value = None
        mock_create_dict.return_value = {'habit_name': 'new_test_habit', 'user_ID': 1, 'category_ID': 1, 'description': 'A test habit', 'creation_date': mock_creation_date}

        expected_data = {'habit_name': 'new_test_habit', 'user_ID': 1, 'category_ID': 1, 'description': 'A test habit', 'creation_date': mock_creation_date}
        
        mock_main_screen.save_habit()

        # Assert statements for adding 1 new habit
        mock_get_category_ID.assert_called_once_with('Test category', 1)
        mock_insert_data.assert_called_once_with("habits", expected_data)
        mock_showerror.assert_not_called()
        mock_showinfo.assert_called_once_with("Success", "Habit: {} successfully saved".format('new_test_habit'))
        mock_main_screen.popup.destroy.assert_called_once()

    @mock.patch.object(MySQLDatabase,'insert_data')
    @mock.patch.object(MySQLDatabase,'get_category_ID')
    @mock.patch.object(MySQLDatabase,'get_habit_ID')
    @mock.patch('tkinter.messagebox.showerror')
    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch('tkinter.Tk')
    def test_save_habit_habit_already_existing(self, mock_tk, mock_showinfo, mock_showerror, mock_get_habit_ID, mock_get_category_ID, mock_insert_data):
        print(" Running test_save_habit_one_added")
        
        mock_popup_instance = mock_tk.return_value
        mock_main_screen = Main_screen(isTest=True)
        mock_main_screen.db = self.db
        mock_main_screen.popup = mock_popup_instance
        mock_main_screen.user_ID = 1        

        # create mock Entry widgets
        mock_main_screen.entry_habit_name = Mock()
        mock_main_screen.entry_description = Mock()
        mock_main_screen.category_var = Mock()
        
        # configure mock Entry widgets to return desired values when get() is called
        mock_main_screen.entry_habit_name.get.return_value = 'new_test_habit'
        mock_main_screen.entry_description.get.return_value = 'A test habit'
        mock_main_screen.category_var.get.return_value = 'Test category'

        mock_main_screen.category_ID = 1
        mock_get_category_ID.return_value = 1
        mock_get_habit_ID.return_value = 1
        
        mock_main_screen.save_habit()

        # Assert statements for adding 1 new habit
        mock_get_category_ID.assert_called_once_with('Test category', 1)
        mock_get_habit_ID.assert_called_once_with(1, 'new_test_habit')
        mock_showerror.assert_called_once_with("Error", "You already have a habit with the same name stored. Please choose a different name.")

    @mock.patch.object(MySQLDatabase,'insert_data')
    @mock.patch('tkinter.messagebox.showerror')
    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch('tkinter.Tk')
    @mock.patch('tkinter.Toplevel')
    @mock.patch.object(Category,'create_dict')
    def test_save_category(self, mock_create_dict, mock_toplevel, mock_tk, mock_showinfo, mock_showerror, mock_insert_data):
        print(" Running test_save_category_one_added")
        
        mock_add_cat_pop_instance = mock_toplevel

        mock_main_screen = Main_screen(isTest=True)
        mock_main_screen.db = self.db
        mock_main_screen.add_cat_pop = mock_add_cat_pop_instance
        mock_main_screen.user_ID = 1        

        # create mock Entry widgets
        mock_main_screen.entry_category_name = Mock()
        mock_main_screen.entry_description = Mock()
        
        # configure mock Entry widgets to return desired values when get() is called
        mock_main_screen.entry_category_name.get.return_value = 'new_test_category'
        mock_main_screen.entry_description.get.return_value = 'A test category'

        mock_create_dict.return_value = {'category_name': 'new_test_category', 'user_ID': 1, 'creation_date': '2023-05-09T16:14:00', 'description': 'A test category'}

        expected_data = {'category_name': 'new_test_category', 'user_ID': 1, 'creation_date': '2023-05-09T16:14:00', 'description': 'A test category'}

        mock_main_screen.save_category()

        # Assert statements for adding 1 new category
        mock_insert_data.assert_called_once_with('category', expected_data)
        mock_showinfo.assert_called_once_with("Success", "Category: {} successfully saved".format('new_test_category')) 
        mock_showerror.assert_not_called()

    @mock.patch('tkinter.ttk.Treeview')
    @mock.patch('tkinter.messagebox.showerror')
    @mock.patch('tkinter.messagebox.showinfo')
    @mock.patch.object(MySQLDatabase,'update_data')
    @mock.patch.object(MySQLDatabase,'check_value')
    @mock.patch.object(MySQLDatabase,'get_streak')
    @mock.patch.object(MySQLDatabase,'get_active_habit_ID')
    @mock.patch.object(MySQLDatabase,'get_habit_ID')
    def test_check_daily_habit(self, mock_get_habit_ID, mock_get_active_habit_ID, mock_get_streak,mock_check_value,mock_update_data, mock_showinfo, mock_showerror,mock_treeview):
        print(" Running test_check_daily_habit")

        treeview_mock_object = mock.MagicMock(name="mock_treeview")
        treeview_mock_object.selection.return_value =[("test_habit", 0, "daily", timedelta(hours=23))]
        treeview_mock_object.item.return_value = {"values": ("test_habit", 0, "daily", timedelta(hours=23))}
        
        mock_main_screen = Main_screen(isTest=True)
        mock_main_screen.db = self.db
        mock_main_screen.active_habits_tree = treeview_mock_object

        mock_main_screen.user_ID = 1

        mock_get_habit_ID.return_value = (5,)
        mock_get_active_habit_ID.return_value = 5
        mock_get_streak.return_value = 0
        mock_check_value.return_value = [(datetime.datetime.now(),)]
        mock_check_value.return_value = [(datetime.datetime.now()+timedelta(hours=23),)]

        expected_new_streak = 1
        expected_new_update_expiry = datetime.datetime.now()+timedelta(hours=47)

        expected_next_check = datetime.datetime.now()+timedelta(hours=23) -datetime.datetime.now()
      
        expected_data = {"streak": expected_new_streak,
                                "last_check": datetime.datetime.now().replace(microsecond=0),
                                "update_expiry": expected_new_update_expiry}

        
        mock_main_screen.check_habit()

        # Assert statements for checking 1 active habit for the first time(streak=0 and daily habit
        mock_update_data.assert_called_once_with("active_user_habits",expected_data,"active_habits", 5)
        mock_showinfo.assert_called_once()
        mock_showerror.assert_not_called()


if __name__ == '__main__':
    unittest.main()


   