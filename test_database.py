from database import MySQLDatabase
import unittest
import datetime
from unittest import TestCase, mock
from unittest.mock import patch, Mock
import mysql.connector
from mysql.connector import errorcode



class TestMySQLDatabase(unittest.TestCase):
    @classmethod
    def setUp(self):
        print("\nRunning setUp method..")
        self.db = MySQLDatabase('localhost','root','Mannheim')
        self.db.cursor = mock.MagicMock()
        self.db.connection = mock.MagicMock()
    @classmethod
    def tearDown(self):
        print("Running tear down method")

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_insert_data(self, mock_connect, mock_disconnect):
        print("Running insert_data method")
        # Mock data and table name
        data = {'ID': 1, 'username': 'test_user'}
        table_name = 'user_table'

        # Call the function
        self.db.insert_data(table_name, data)

        # Assert that the SQL query was constructed correctly
        expected_query = "INSERT INTO user_table (ID, username) VALUES (%s, %s)"
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (1, 'test_user'))

        # Assert that the connection was committed
        self.db.connection.commit.assert_called_once()

        mock_disconnect.assert_called_once()
    
    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_update_data(self, mock_connect, mock_disconnect):
        print("Running update_data method")
        # Mock data and table name
        table_name = 'user_table'
        data = {'username': 'test_user'}
        object = 'user'
        ID = 1

        # Call the function
        self.db.update_data(table_name, data, object, ID)

        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with("UPDATE user_table SET username = 'test_user' WHERE user_ID = 1")
        self.db.connection.commit.assert_called_once()

        mock_disconnect.assert_called_once()
    
    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_check_value_with_results(self, mock_connect, mock_disconnect):
        print("Running test_check_value test")
        # Mock data for attributes
        searched_value = "username"
        table = "user_table"
        column = "user_ID"
        value = 1
        
        # Mock the database cursor's fetchall() method to return an empty list
        self.db.cursor.fetchall.return_value = ['user_1',]

        # Call the method being tested
        results = self.db.check_value(searched_value, table, column, value)

        #self.db.check_value(searched_value, table, column, value)
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with('SELECT username FROM user_table WHERE user_ID = %s', (1,))
        self.assertNotEqual(len(results), 0)
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    def test_get_user_credentials_user_found(self, mock_connect):
        print("Running test_get_user_ID")
        user_ID = 1
        expected_query = f"SELECT user_ID, username, first_name, last_name, password, email, phone_number, created_time, last_update FROM user_table WHERE user_ID = %s"
        self.db.cursor.fetchone.return_value = (1, 'Sippi', 'Marc', 'Fischer', 'password123', 'mafi@email.com', '555-555-5555', '2022-04-28 12:00:00', '2022-04-28 12:00:00')
        # Check that the function returned the expected dictionary
        expected_dict = {
            'user_ID': 1,
            'username': 'Sippi',
            'first_name': 'Marc',
            'last_name': 'Fischer',
            'password': 'password123',
            'email': 'mafi@email.com',
            'phone_number': '555-555-5555',
            'created_time': '2022-04-28 12:00:00',
            'last_update': '2022-04-28 12:00:00'
        }


        result_dict = self.db.get_user_credentials(user_ID)
        
        mock_connect.assert_called_once()

        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))
        self.assertEqual(result_dict, expected_dict)

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_get_userID_user_found(self, mock_connect, mock_disconnect):
        print("Running test_get_user_ID")
        username = "user_1"
        expected_query = "SELECT user_ID FROM user_table WHERE username = %s"
        self.db.cursor.fetchone.return_value = [1,]
        expected_userID = 1
        
        results = self.db.get_userID(username)
        mock_connect.assert_called_once()

        self.db.cursor.execute.assert_called_once_with(expected_query, (username,))
        self.assertEqual(results, expected_userID)

        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_get_user_habits(self, mock_connect, mock_disconnect):
        print("Running test_get_user_habits")
        user_ID = 1
        expected_query = """SELECT habits.habit_ID, habits.habit_name, habits.description, habits.creation_date, category.category_name
	                    FROM habits  
                        INNER JOIN category ON habits.category_ID = category.category_ID
                        WHERE habits.user_ID = %s OR habits.user_ID = 99;                
                """
        expected_result = [(2, 'Singing', 'Singing', datetime.datetime(2023, 3, 25, 15, 0), 'Art'), (3, 'Reading', 'Reading', datetime.datetime(2023, 3, 10, 0, 0), 'Any')]

        self.db.cursor.fetchall.return_value = [(2, 'Singing', 'Singing', datetime.datetime(2023, 3, 25, 15, 0), 'Art'), (3, 'Reading', 'Reading', datetime.datetime(2023, 3, 10, 0, 0), 'Any')]

        result = self.db.get_user_habits(user_ID)
        
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))
        
        self.assertEqual(result, expected_result)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_get_habit_ID(self, mock_connect, mock_disconnect):
        print("Running test_get_habit_ID")
        user_ID = 1
        habit_name = "Sports"
        expected_query = f'''SELECT active_user_habits.habit_ID FROM active_user_habits
                    INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                    WHERE habits.habit_name = '{habit_name}' AND (habits.user_ID = {user_ID} OR habits.user_ID = 99)
                '''

        self.db.cursor.fetchone.return_value = 2

        expected_return = self.db.get_habit_ID(user_ID, habit_name) 

        self.db.cursor.execute.assert_called_once_with(expected_query)
        
        self.assertEqual(expected_return, 2)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_active_habits(self, mock_connect, mock_disconnect):
        print("Running test_get_active_habits")
        user_ID = 1

        expected_query = """SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        WHERE active_user_habits.user_ID = %s AND active_user_habits.status != 'deleted';
                """
        self.db.cursor.fetchall.return_value = [(2, 'Homeworkout', datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 29, 22, 53, 55), 19, 'daily', 'in progress')]
        expected_return = [(2, 'Homeworkout', datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 29, 22, 53, 55), 19, 'daily', 'in progress')]
        return_value = self.db.get_active_habits(user_ID) 


        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))
        
        self.assertEqual(return_value, expected_return)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()
    
    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_global_active_habits(self, mock_connect, mock_disconnect):
        print("Running test_get_global_active_habits")
        interval_ID = 1

        expected_query = f"""SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status, user_table.username
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        INNER JOIN user_table ON active_user_habits.user_ID = user_table.user_ID
                        WHERE active_user_habits.interval_ID = {interval_ID}   
                        ORDER BY active_user_habits.streak DESC;
                """
        self.db.cursor.fetchall.return_value = [(2, 'Homeworkout', datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 29, 22, 53, 55), 19, 'daily', 'in progress')]
        expected_return = [(2, 'Homeworkout', datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 29, 22, 53, 55), 19, 'daily', 'in progress')]
        return_value = self.db.get_global_active_habits(interval_ID) 

        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)
        
        self.assertEqual(return_value, expected_return)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_all_active_habits(self, mock_connect, mock_disconnect):
        print("Running test_get_all_active_habits")
        user_ID = 1

        expected_query = """SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status, active_user_habits.goal_streak
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        WHERE active_user_habits.user_ID = %s
                        ORDER BY active_user_habits.streak DESC;
                """
        self.db.cursor.fetchall.return_value = [(3, 'Smoking', datetime.datetime(2023, 4, 28, 17, 33, 4), datetime.datetime(2023, 4, 27, 22, 53, 55), datetime.datetime(2023, 4, 28, 22, 53, 55), 44, 'daily', 'deleted', 60)]
        expected_return = [(3, 'Smoking', datetime.datetime(2023, 4, 28, 17, 33, 4), datetime.datetime(2023, 4, 27, 22, 53, 55), datetime.datetime(2023, 4, 28, 22, 53, 55), 44, 'daily', 'deleted', 60)]
        return_value = self.db.get_all_active_habits(user_ID) 

        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))
        
        self.assertEqual(return_value, expected_return)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_global_active_habits(self, mock_connect, mock_disconnect):
        print("Running test_get_global_active_habits")
        interval_ID = 1

        expected_query = f"""SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status, user_table.username
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        INNER JOIN user_table ON active_user_habits.user_ID = user_table.user_ID
                        WHERE active_user_habits.interval_ID = {interval_ID}   
                        ORDER BY active_user_habits.streak DESC;
                """
        self.db.cursor.fetchall.return_value = [(2, 'Homeworkout', datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 29, 22, 53, 55), 19, 'daily', 'in progress')]
        expected_return = [(2, 'Homeworkout', datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 29, 22, 53, 55), 19, 'daily', 'in progress')]
        return_value = self.db.get_global_active_habits(interval_ID) 

        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)
        
        self.assertEqual(return_value, expected_return)

        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_active_habit_ID_one_habit_found(self, mock_connect, mock_disconnect):
        print("Running test_get_active_habit_ID_one_habit_found")
        user_ID = 1
        habit_ID = 2
        status = "in progress"

        expected_query = f""" SELECT active_habits_ID FROM active_user_habits
                    WHERE user_ID = {user_ID} AND habit_ID = {habit_ID} AND status = "{status}";
        """ 
        self.db.cursor.fetchone.return_value = (5,)
        expected_return = 5
        return_value = self.db.get_active_habit_ID(user_ID, habit_ID, status) 

        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)
        
        self.assertEqual(return_value, expected_return)

        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_streak_one_habit_found(self, mock_connect, mock_disconnect):
        print("Running test_get_streak_one_habit_found")
        active_habits_ID = 1

        expected_query = f"""SELECT streak FROM active_user_habits
                    WHERE active_habits_ID = {active_habits_ID}"""

        self.db.cursor.fetchone.return_value = (20,)
        expected_return = 20
        return_value = self.db.get_streak(active_habits_ID) 

        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)
        
        self.assertEqual(return_value, expected_return)

        mock_disconnect.assert_called_once()
        

        

    # @mock.patch.object(MySQLDatabase, 'connect')
    # @mock.patch.object(MySQLDatabase, 'disconnect')
    # def test_check_value_without_results(self, mock_connect, mock_disconnect):
    #     print("Running check_value test")
    #     # Mock data for attributes
    #     searched_value = "username"
    #     table = "user_table"
    #     column = "user_ID"
    #     value = 1

    #     # Mock the database cursor's fetchall() method to return an empty list
    #     self.db.cursor.fetchall.return_value = []

    #     # Call the method being tested
    #     results = self.db.check_value(searched_value, table, column, value)

    #     # Capture the printed output
    #     captured_output = io.StringIO()
    #     sys.stdout = captured_output
    #     print("User not found.")
    #     sys.stdout = sys.__stdout__

    #     # Assert that the expected output was printed
    #     self.assertEqual(captured_output.getvalue().strip(), "User not found.")

    #     #self.db.check_value(searched_value, table, column, value)
    #     mock_connect.assert_called_once()
    #     self.db.cursor.execute.assert_called_once_with('SELECT username FROM user_table WHERE user_ID = %s', (1,))
    #     self.assert_called_once_with(print("User not found."))
    #     mock_disconnect.assert_called_once()

        












    # @mock.patch.object(MySQLDatabase, 'connect')
    # @mock.patch.object(MySQLDatabase, 'disconnect')
    # @mock.patch.object(MySQLDatabase, 'initialize_database')
    # # @mock.patch.object(MySQLDatabase, 'cursor')
    # def test_create_database(self, mock_initialize_database, mock_disconnect, mock_connect):
    #     print("Running test_create_database")
    #     self.db.cursor.execute.return_value.rowcount = 1
    #     self.db.create_database('test_database')
    #     mock_connect.assert_called_once()
    #     self.db.cursor.execute.assert_called_once_with(f"CREATE DATABASE IF NOT EXISTS test_database")
    #     mock_initialize_database.assert_called_once_with('test_database')
    #     mock_disconnect.assert_called_once()

    if __name__ == '__main__':
        unittest.main()




    # def test_insert_data(self):
    #     # create a mock database object
    #     db = MySQLDatabase('mock_db', 'mock_user', 'mock_password', 'mock_host')

    #     # mock the connect and disconnect methods
    #     with patch.object(db, 'connect'):
    #         with patch.object(db, 'disconnect'):
    #             # example data
    #             table_name = 'example_table'
    #             data = {'ID': 1, 'username': 'Marc'}

    #             # expected SQL query
    #             expected_query = "INSERT INTO example_table (ID, username) VALUES (%s, %s)"

    #             # call the insert_data method
    #             db.insert_data(self, table_name, data)

    #             # assert that the query was constructed correctly
    #             self.assertEqual(db.cursor._last_executed, expected_query)



