from database import MySQLDatabase
import unittest
import datetime
from unittest import mock

class TestMySQLDatabase(unittest.TestCase):
    @classmethod
    def setUp(self):
        print("\nRunning setUp method..")
        self.db = MySQLDatabase('localhost','root','password')
        self.db.cursor = mock.MagicMock()
        self.db.connection = mock.MagicMock()
    @classmethod
    def tearDown(self):
        print("Running tear down method")

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_insert_data(self, mock_connect, mock_disconnect):
        """
        Test case for the `insert_data` method of `MySQLDatabase` class.
        """
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

        # Assert that the disconnect function was called  
        mock_disconnect.assert_called_once()
    
    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_update_data(self, mock_connect, mock_disconnect):
        """
        Test case for the `update_data` method of `MySQLDatabase` class.
        """
        print("Running update_data method")
        # Mock data and table name
        table_name = 'user_table'
        data = {'username': 'test_user'}
        object = 'user'
        ID = 1

        # Call the function
        self.db.update_data(table_name, data, object, ID)

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with("UPDATE user_table SET username = 'test_user' WHERE user_ID = 1")
        self.db.connection.commit.assert_called_once()
        mock_disconnect.assert_called_once()
    
    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_check_value_with_results(self, mock_connect, mock_disconnect):
        """
        Test case for the `check_value` method of `MySQLDatabase` class.
        """
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

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with('SELECT username FROM user_table WHERE user_ID = %s', (1,))
        self.assertNotEqual(len(results), 0)
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    def test_get_user_credentials_user_found(self, mock_connect):
        """
        Test case for the `get_user_credentials` method of `MySQLDatabase` class.
        """
        print("Running test_get_user_ID")
        user_ID = 1

        # Mock the expected SQL query and result
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

        # Call the function
        result_dict = self.db.get_user_credentials(user_ID)

        # Assert that the method calls were made correctly      
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))
        self.assertEqual(result_dict, expected_dict)

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_get_userID_user_found(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_user_ID` method of `MySQLDatabase` class.
        """
        print("Running test_get_user_ID")
        # Mock data 
        username = "user_1"

        # Mock the expected SQL query and result
        expected_query = "SELECT user_ID FROM user_table WHERE username = %s"
        self.db.cursor.fetchone.return_value = [1,]
        expected_userID = 1
        
        # Call the function
        results = self.db.get_userID(username)

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (username,))
        self.assertEqual(results, expected_userID)
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_get_user_habits(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_user_habits` method of `MySQLDatabase` class.
        """
        print("Running test_get_user_habits")
        # Mock data 
        user_ID = 1

        # Mock the expected SQL query and result
        expected_query = """SELECT habits.habit_ID, habits.habit_name, habits.description, habits.creation_date, category.category_name
	                    FROM habits  
                        INNER JOIN category ON habits.category_ID = category.category_ID
                        WHERE habits.user_ID = %s OR habits.user_ID = 99;                
                """
        expected_result = [(2, 'Singing', 'Singing', datetime.datetime(2023, 3, 25, 15, 0), 'Art'), (3, 'Reading', 'Reading', datetime.datetime(2023, 3, 10, 0, 0), 'Any')]

        self.db.cursor.fetchall.return_value = [(2, 'Singing', 'Singing', datetime.datetime(2023, 3, 25, 15, 0), 'Art'), (3, 'Reading', 'Reading', datetime.datetime(2023, 3, 10, 0, 0), 'Any')]

        # Call the function
        result = self.db.get_user_habits(user_ID)

        # Assert that the method calls were made correctly        
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))        
        self.assertEqual(result, expected_result)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')
    def test_get_habit_ID(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_habit_ID` method of `MySQLDatabase` class.
        """
        print("Running test_get_habit_ID")
        # Mock data 
        user_ID = 1
        habit_name = "Sports"

        # Mock the expected SQL query and result
        expected_query = f'''SELECT habit_ID FROM habits
                WHERE habit_name = '{habit_name}' AND (user_ID = {user_ID} OR user_ID = 99);
                '''

        self.db.cursor.fetchone.return_value = 2

        # Call the function
        expected_return = self.db.get_habit_ID(user_ID, habit_name) 

        self.db.cursor.execute.assert_called_once_with(expected_query)

        # Assert that the method calls were made correctly        
        self.assertEqual(expected_return, 2)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_active_habits(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_active_habits` method of `MySQLDatabase` class.
        """
        print("Running test_get_active_habits")
        # Mock data 
        user_ID = 1

        # Mock the expected SQL query and result
        expected_query = """SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        WHERE active_user_habits.user_ID = %s AND active_user_habits.status != 'deleted';
                """
        self.db.cursor.fetchall.return_value = [(2, 'Homeworkout', datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 29, 22, 53, 55), 19, 'daily', 'in progress')]
        expected_return = [(2, 'Homeworkout', datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 28, 17, 33, 13), datetime.datetime(2023, 4, 29, 22, 53, 55), 19, 'daily', 'in progress')]
        
        # Call the function
        return_value = self.db.get_active_habits(user_ID) 

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))        
        self.assertEqual(return_value, expected_return)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()
    
    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_global_active_habits(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_global_active_habits` method of `MySQLDatabase` class.
        """
        print("Running test_get_global_active_habits")
        # Mock data 
        interval_ID = 1

        # Mock the expected SQL query and result
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
        
        # Call the function
        return_value = self.db.get_global_active_habits(interval_ID) 

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)        
        self.assertEqual(return_value, expected_return)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_all_active_habits(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_all_active_habits` method of `MySQLDatabase` class.
        """
        print("Running test_get_all_active_habits")
        # Mock data 
        user_ID = 1

        # Mock the expected SQL query and result
        expected_query = """SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status, active_user_habits.goal_streak
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        WHERE active_user_habits.user_ID = %s
                        ORDER BY active_user_habits.streak DESC;
                """
        self.db.cursor.fetchall.return_value = [(3, 'Smoking', datetime.datetime(2023, 4, 28, 17, 33, 4), datetime.datetime(2023, 4, 27, 22, 53, 55), datetime.datetime(2023, 4, 28, 22, 53, 55), 44, 'daily', 'deleted', 60)]
        expected_return = [(3, 'Smoking', datetime.datetime(2023, 4, 28, 17, 33, 4), datetime.datetime(2023, 4, 27, 22, 53, 55), datetime.datetime(2023, 4, 28, 22, 53, 55), 44, 'daily', 'deleted', 60)]
        
        # Call the function
        return_value = self.db.get_all_active_habits(user_ID) 

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))        
        self.assertEqual(return_value, expected_return)
        mock_connect.assert_called_once()
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_global_active_habits(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_global_active_habits` method of `MySQLDatabase` class.
        """
        print("Running test_get_global_active_habits")
        # Mock data 
        interval_ID = 1

        # Mock the expected SQL query and result
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
        
        # Call the function
        return_value = self.db.get_global_active_habits(interval_ID) 

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)        
        self.assertEqual(return_value, expected_return)
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_active_habit_ID_one_habit_found(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_active_habit_ID` method of `MySQLDatabase` class.
        """
        print("Running test_get_active_habit_ID_one_habit_found")
        # Mock data 
        user_ID = 1
        habit_ID = 2
        status = "in progress"

        # Mock the expected SQL query and result
        expected_query = f""" SELECT active_habits_ID FROM active_user_habits
                    WHERE user_ID = {user_ID} AND habit_ID = {habit_ID} AND status = "{status}";
        """ 
        self.db.cursor.fetchone.return_value = (5,)
        expected_return = 5
        
        # Call the function
        return_value = self.db.get_active_habit_ID(user_ID, habit_ID, status) 

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)        
        self.assertEqual(return_value, expected_return)
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_streak_one_habit_found(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_streak` method of `MySQLDatabase` class.
        """
        print("Running test_get_streak_one_habit_found")
        # Mock data 
        active_habits_ID = 1

        # Mock the expected SQL query and result
        expected_query = f"""SELECT streak FROM active_user_habits
                    WHERE active_habits_ID = {active_habits_ID}"""

        self.db.cursor.fetchone.return_value = (20,)
        expected_return = 20
        
        # Call the function
        return_value = self.db.get_streak(active_habits_ID) 


        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)        
        self.assertEqual(return_value, expected_return)
        mock_disconnect.assert_called_once()
        
    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_delete_habit(self, mock_connect, mock_disconnect):
        """
        Test case for the `delete_habit` method of `MySQLDatabase` class.
        """
        print("Running test_delete_habit")
        # Mock data 
        habit_ID = 1

        # Mock the expected SQL query
        expected_query = f"""DELETE FROM habits WHERE habit_ID = {habit_ID};"""

        # Call the function
        self.db.delete_habit(habit_ID)

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)        
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_update_value(self, mock_connect, mock_disconnect):
        """
        Test case for the `update_value` method of `MySQLDatabase` class.
        """
        print("Running test_update_value")
        # Mock data 
        table_name = "user_table"
        data = {"username":"Marc", "phone_number": "12232131"}
        column1 = "username"
        column2 = "phone_number"
        value1 = "Sippi"
        value2 = "7878997"

        # Mock the expected SQL query
        expected_query = f"UPDATE {table_name} SET username = 'Marc', phone_number = '12232131' WHERE user_table.username = 'Sippi' AND user_table.phone_number = '7878997';"

        # Call the function
        self.db.update_value(table_name, data, column1, column2, value1, value2)

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)        
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_user_categories(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_user_categories` method of `MySQLDatabase` class.
        """
        print("Running test_get_user_categories")
        # Mock data 
        user_ID = 1

        # Mock the expected SQL query and result
        expected_query = """SELECT category.category_ID, category.category_name, category.description, category.creation_date
	                    FROM category  
                        WHERE category.user_ID = %s OR category.user_ID = 99;
                """ 
        
        self.db.cursor.fetchall.return_value = [(1, 'Art', 'Art', datetime.datetime(2023, 3, 10, 0, 0)), (2, 'Sport', 'Sport', datetime.datetime(2023, 3, 10, 0, 0)), (3, 'Entertainment', 'Entertainment', datetime.datetime(2023, 3, 10, 0, 0)), (4, 'Finance', 'Finance', datetime.datetime(2023, 3, 10, 0, 0)), (5, 'Health', 'Health', datetime.datetime(2023, 3, 10, 0, 0)), (6, 'Work', 'Work', datetime.datetime(2023, 3, 10, 0, 0)), (7, 'Food', 'Food', datetime.datetime(2023, 3, 10, 0, 0)), (8, 'Any', 'Any', datetime.datetime(2023, 3, 10, 0, 0)), (9, 'Traveling', 'Traveling', datetime.datetime(2023, 3, 15, 10, 0))]
        expected_return = [(1, 'Art', 'Art', datetime.datetime(2023, 3, 10, 0, 0)), (2, 'Sport', 'Sport', datetime.datetime(2023, 3, 10, 0, 0)), (3, 'Entertainment', 'Entertainment', datetime.datetime(2023, 3, 10, 0, 0)), (4, 'Finance', 'Finance', datetime.datetime(2023, 3, 10, 0, 0)), (5, 'Health', 'Health', datetime.datetime(2023, 3, 10, 0, 0)), (6, 'Work', 'Work', datetime.datetime(2023, 3, 10, 0, 0)), (7, 'Food', 'Food', datetime.datetime(2023, 3, 10, 0, 0)), (8, 'Any', 'Any', datetime.datetime(2023, 3, 10, 0, 0)), (9, 'Traveling', 'Traveling', datetime.datetime(2023, 3, 15, 10, 0))]
        
        # Call the function
        return_value = self.db.get_user_categories(user_ID) 

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))
        self.assertEqual(return_value, expected_return)        
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_user_categories_name(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_user_categories_name` method of `MySQLDatabase` class.
        """
        print("Running test_get_user_categories_name")
        # Mock data 
        user_ID = 1
        
        expected_query = """SELECT category.category_name
	                    FROM category  
                        WHERE category.user_ID = %s OR category.user_ID = 99;      
                """    
        
        # Mock the expected SQL query and result
        self.db.cursor.fetchall.return_value = [('Art',), ('Sport',), ('Entertainment',), ('Finance',), ('Health',), ('Work',), ('Food',), ('Any',), ('Traveling',)]
        expected_return = [('Art',), ('Sport',), ('Entertainment',), ('Finance',), ('Health',), ('Work',), ('Food',), ('Any',), ('Traveling',)]
        
        # Call the function
        return_value = self.db.get_user_categories_name(user_ID) 

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query, (user_ID,))
        self.assertEqual(return_value, expected_return)        
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_get_category_ID(self, mock_connect, mock_disconnect):
        """
        Test case for the `get_category_ID` method of `MySQLDatabase` class.
        """
        print("Running test_get_category_ID")
        # Mock data 
        category_name = "Art"
        user_ID = 1

        # Mock the expected SQL query and result        
        expected_query = "SELECT category_ID FROM category WHERE category_name = 'Art' AND (user_ID = 1 OR user_ID = 99);"
        
        self.db.cursor.fetchone.return_value = (1,)
        expected_return = 1
        
        # Call the function
        return_value = self.db.get_category_ID(category_name, user_ID) 
        
        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)
        self.assertEqual(return_value, expected_return)        
        mock_disconnect.assert_called_once()

    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_delete_category(self, mock_connect, mock_disconnect):
        """
        Test case for the `delete_category` method of `MySQLDatabase` class.
        """
        print("Running test_delete_category")
        # Mock data 
        category_ID = 1

        # Mock the expected SQL query and result    
        expected_query = f"""DELETE FROM category WHERE category_ID = 1;"""

        # Call the function
        self.db.delete_category(category_ID)

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(expected_query)        
        mock_disconnect.assert_called_once()


    @mock.patch.object(MySQLDatabase, 'connect')
    @mock.patch.object(MySQLDatabase, 'disconnect')  
    def test_execute_query(self, mock_connect, mock_disconnect):
        """
        Test the execute_query method of the MySQLDatabase class
        
        This method tests whether the execute_query method of the MySQLDatabase class
        correctly executes a given query and returns the expected result.
        """
        print("Running test_execute_query")
        
        # Define a test query to execute
        test_query = "SELECT username FROM user_table WHERE user_ID = 1;"

        # Mock the database cursor's fetchone() method to return a specified value
        self.db.cursor.fetchone.return_value = ("user_01",)
        expected_return = ("user_01",)
        
        # Call the function
        return_value = self.db.execute_query(test_query)

        # Assert that the method calls were made correctly
        mock_connect.assert_called_once()
        self.db.cursor.execute.assert_called_once_with(test_query)
        self.assertEqual(return_value, expected_return)
        mock_disconnect.assert_called_once()    

    if __name__ == '__main__':
        unittest.main()








