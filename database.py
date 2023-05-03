import mysql.connector
import time
from tkinter import messagebox

class MySQLDatabase:
    """
    A class for interacting with a MySQL Database.

    Attributes:
        host (str): The hostname of the MySQL server.
        user (str): The username for the MySQL server.
        password (str): The password for the MySQL server.
        database (Optional[str]): The name of the MySQL database to use.

    Methods:
        __init__: Initializes the MySQLDatabase object.
        connect: Connects to the MySQL server.
        disconnect: Disconnects from the MySQL server.
        create_database: Creates a new database on the MySQL server if it not allready exists.
        initialize_database: Initializes the database by creating tables and and inserts sample data using Insert statements.
        create_table: Creates a new table in the MySQL database.
        delete_table: Deletes a table from the MySQL database.
        insert_data: Inserts data into a table in the MySQL database.
        update_data: Updates data in a table in the MySQL database.
        check_value: Checks if a given value exists in a table in the MySQL database.
        get_user_credentials: Retrieves user credentials from the MySQL database.
        get_userID: Retrieves the user ID for a given username from the MySQL database.
        get_user_habits: Retrieves all habits for a given user from the MySQL database.
        get_habit_ID: Retrieves the habit ID for a given habit name and user ID from the MySQL database.
        get_active_habits: Retrieves all active habits for a given user from the MySQL database.
        get_global_active_habits: Retrieves all global active habits from the MySQL database.
        get_all_active_habits: Retrieves all active habits from the MySQL database.
        get_active_habit_ID: Retrieves the active habit ID for a given habit ID and user ID from the MySQL database.
        get_streak: Retrieves the current streak for a given user and habit from the MySQL database.
        delete_habit: Deletes a habit for a given user from the MySQL database.
        update_value: Updates the value for a given habit for a given user in the MySQL database.
        get_user_categories: Retrieves all categories for a given user from the MySQL database.
        get_user_categories_name: Retrieves only the names of all categories for a given user from the MySQL database.
        get_category_ID: Retrieves the category ID for a given category name and user ID from the MySQL database.
        delete_category: Deletes a category for a given user from the MySQL database.
        execute_query: Executes a custom SQL query on the MySQL database.
    """
    def __init__(self, host, user, password, database = None):
        """
        Initializes a new MySQLDatabase object.

        Args:
            host (str): The hostname of the MySQL server.
            user (str): The username for the MySQL server.
            password (str): The password for the MySQL server.
            database (Optional[str]): The name of the MySQL database to use.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """
        Connects to the MySQL database using the credentials specified during object initialization.

        Raises:
            Exception: If the connection to the database fails.
        """
        try:
            self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
            )
        except Exception as e: 
            messagebox.showerror("Error","There is something wrong with your database credentials. Please check and try again.")
            raise Exception("Failed to connect to MySQL database. Please check your credentials and try again.")
        self.cursor = self.connection.cursor(buffered=True)

    def disconnect(self):
        """
        Disconnects from the MySQL database.

        Note:
            This function does not raise any exceptions.
        """

        if self.connection is not None:
            self.connection.close()
        if self.cursor is not None:
            self.cursor.close()
    
    
    def create_database(self,new_database):
        """
        Creates a new MySQL database with the given name if it does not already exist, and initializes the database with the necessary tables and sample data.

        Args:
            new_database (str): The name of the new database to be created.

        Note:
            The initialization function is called only if a new database is created.

        Raises:
            Exception: If there is an error while connecting to the database or initializing it.
        """
        try:
            self.connect()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_database}")
            self.database = new_database
            if self.cursor.rowcount == 1:
                self.initialize_database(self.database) # Call database initialization function if a new database was created
                messagebox.showinfo("Success", "Database created. You can go on and login/register.")
        finally:
            self.disconnect()

    def initialize_database(self,database):
        """
        Initializes the given MySQL database with the necessary tables and sample data by executing the SQL statements in a file.

        Args:
            database (str): The name of the database to be initialized.

        Raises:
            Exception: If there is an error while executing any of the SQL statements in the file.
        """
        
        # Read the contents of the file that contains the SQL statements database_tables.txt which has to be located in the same folder
        with open('database_tables.txt', 'r') as f:
            sql = f.read()

        # Split the SQL statements by the semicolon delimiter and remove any leading/trailing white space
        statements = []
        statements.append(f"USE {database};")
        statements += [x.strip() for x in sql.split(';')]

        # Execute each SQL statement
        for statement in statements:
            #print(statement)
            try:
                self.cursor.execute(statement)
                self.connection.commit()
                print(f"Table created")
            except Exception as e:
                print(f"An error occurred while executing SQL statement: {statement}")
                print(f"Error message: {str(e)}")

        # Insert all predefinded insert statements using the insert.txt file. First open txt file:
        with open('inserts.txt', 'r') as f:
            inserts = f.readlines()
        # Execeute each query in the file 
        counter = 0
        for insert in inserts:
            try:
                counter +=1
                self.connect()
                query = insert
                self.cursor.execute(query)
                self.connection.commit()
                rows_affected = self.cursor.rowcount
                if rows_affected == 0:
                    print("No rows were inserted into the database.")
                else:
                    print(f"{rows_affected} rows were inserted into the database.")
                print(f"Insert {counter} executed, {query}")
                time.sleep(0.15)
            except Exception as e:
                print("An error occurred:", e)

    def create_table(self, table_name, *columns):
        """
        Creates a new table in the database if it doesn't already exist.

        Args:
            table_name (str): The name of the table to be created.
            *columns (str): One or more column definitions, each formatted as a string like 'column_name column_type', separated by commas.

        Returns:
            None
        """
        self.connect()
        self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = self.cursor.fetchone()
        if result:
            print(f"Table '{table_name}' already exists")
        else:
            # Construct the SQL query for creating the table
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})" 
            # Execute the SQL query to create the table
            self.cursor.execute(query)
            print(f"Table '{table_name}' created successfully")
        self.disconnect()
    
    def delete_table(self, table_name):
        """
        Deletes a table from the database.

        Args:
            table_name (str): The name of the table to be deleted.

        Returns:
            None
        """
        self.connect()
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Table '{table_name}' deleted successfully")
        self.disconnect()
 
 
    # Inserts Values into tables  
    def insert_data(self, table_name, data):
        """
        Inserts a row of data into a table.

        Args:
            table_name (str): The name of the table into which data should be inserted.
            data (dict): A dictionary containing the values to be inserted into the table, with keys corresponding to column names.

        Returns:
            None
        """

        # Establish a connection to the database
        self.connect()

        # Construct the SQL query for inserting data into the table
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data.values()))
        values = tuple(None if v == '' else v for v in data.values()) # set None for empty string values in dict
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Execute the SQL query to insert data into the table
        self.cursor.execute(query, values)
        self.connection.commit()

        # Print the number of rows inserted into the table
        print(f"{self.cursor.rowcount} row(s) inserted into {table_name}.")

        # Disconnct from the datbase
        self.disconnect()

    def update_data(self, table_name, data, object, ID):
        """
        Updates the values of a row in a given table.

        Args:
            table_name (str): The name of the table to update.
            data (dict): A dictionary containing the column names and values to update.
            object (str): The name of the primary key without '_ID'.
            ID (int): The unique primary key value for the row to update.

        Returns:
            None
        """

        # Connect to the database
        self.connect()

        # Construct name of the primary key for where clause
        primary_key = f"{object}_ID"
        
        # Set string for the sql query
        set_str = ", ".join([f"{col_name} = '{col_value}'" for col_name, col_value in data.items()])
        
        # Execute the query for updating values
        self.cursor.execute(f"UPDATE {table_name} SET {set_str} WHERE {primary_key} = {ID}")
        self.connection.commit()

        
        # Disconnect from database 
        self.disconnect()

    def  check_value(self, searched_value, table, column, value):
        """
        Searches for a specific value in a table column.

        Args:
            searched_value (str): The column name to return.
            table (str): The name of the table to search.
            column (str): The name of the column to search.
            value (str): The value to search for in the specified column.

        Returns:
            results (list): A list of tuples containing the search results.
        """
    
        # Establish connection with the database
        self.connect()  
        # Construct query  
        sql = f"SELECT {searched_value} FROM {table} WHERE {column} = %s"
        self.cursor.execute(sql, (value,))
        results = self.cursor.fetchall()

        # Print out the results
        if len(results) > 0:                      
            self.disconnect()
            return results 

        else:
            print("User not found.")
            self.disconnect()
    
    def get_user_credentials(self,user_ID):
        """
        Queries the database for user credentials using the user_ID as the primary key.

        Args:
            user_ID (int): The unique user identifier.

        Returns:
            result_dict (dict): A dictionary containing the user's credentials.
        """
        
        # Establish connection to the database
        self.connect()
        
        # Set variable table to value "user_table" for query.
        table = "user_table"

        # Create list of column names
        column_names = ["user_ID", "username", "first_name", "last_name", "password", "email", "phone_number", "created_time", "last_update"]
        
        # Construct the SQL query
        query = f"SELECT {', '.join(column_names)} FROM {table} WHERE user_ID = %s"
        
        # Execute the query and fetch the results
        # cursor = self.connection.cursor()
        self.cursor.execute(query, (user_ID,))
        result = self.cursor.fetchone()
        
        # Store the results in a dictionary
        if result:
            result_dict = dict(zip(column_names, result))
            print(result_dict)
        else:
            result_dict = {}
        
        self.cursor.close()
        self.connection.close()
        
        return result_dict

    def  get_userID(self, username):
        """
        Retrieves the unique user_ID for a given username.

        Args:
            username (str): The username to search for.

        Returns:
            int: The user_ID for the given username, or None if no matching user is found.
        """
        
        # Establish connection to the database
        self.connect()

        table = "user_table"
        column = "username"

        # query for returning user_ID
        sql = f"SELECT user_ID FROM {table} WHERE {column} = %s"
        self.cursor.execute(sql, (username,))
        result = self.cursor.fetchone()

        # Print out the results
        if len(result) > 0:
            #print("Found user:")
            user_ID = result[0]
            #print(user_ID)
            self.disconnect()
            return user_ID
        # 
        else:
            print("User not found.")
            self.disconnect()
   
    def get_user_habits(self, user_ID):
        """
        Retrieves all stored habits of a given user.

        Args:
            user_ID (int): The user_ID of the user whose habits to retrieve.

        Returns:
            list of tuples: A list of tuples, where each tuple contains information about a habit, including the habit's ID, name, description, creation date, and category name.
        """

        # Establish connection to the database
        self.connect()

        # Query for returning all habits from the user plus the predefined system user habits. The Systemuser has the user_ID 99
        query = """SELECT habits.habit_ID, habits.habit_name, habits.description, habits.creation_date, category.category_name
	                    FROM habits  
                        INNER JOIN category ON habits.category_ID = category.category_ID
                        WHERE habits.user_ID = %s OR habits.user_ID = 99;                
                """
        # Execute query    
        self.cursor.execute(query, (user_ID,))
        habits = self.cursor.fetchall()
        self.disconnect()

        # return list
        return habits
    
    # Function to get a habit_ID by using the habit_name and user_ID
    def get_habit_ID(self, user_ID, habit_name):
        """
        Retrieves the habit_ID for a given habit name and user_ID.

        Args:
            user_ID (int): The user_ID of the user who owns the habit.
            habit_name (str): The name of the habit to search for.

        Returns:
            int: The habit_ID for the given habit name and user_ID, or None if no matching habit is found.
        """

        # Connect to database
        self.connect()

        # Information about user and habit
        self.user_ID = user_ID
        self.habit_name = habit_name
        
        # Set table_name
        table_name = 'habits'
        
        # Construct query for returning the habit_ID 
        query = f'''SELECT active_user_habits.habit_ID FROM active_user_habits
                    INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                    WHERE habits.habit_name = '{habit_name}' AND (habits.user_ID = {user_ID} OR habits.user_ID = 99)
                '''
        
        # Execute query
        self.cursor.execute(query)
        habit_ID = self.cursor.fetchone()

        # Commit changes to the database
        self.connection.commit()

        # Disconnect from database
        self.disconnect()

        # Return the habit_ID
        return habit_ID
    
    def get_active_habits(self, user_ID):
        """
        Returns all stored active habits of a user, excluding those with the status 'deleted'.
        
        Args:
            user_ID (int): The user ID for the user whose active habits are to be retrieved.
        
        Returns:
            A list of tuples, where each tuple represents an active habit and contains the following values:
            - active_habits_ID (int): The ID of the active habit.
            - habit_name (str): The name of the habit.
            - starting_date (datetime.datetime): The date when the user started the habit.
            - last_check (datetime.datetime): The date when the user last checked in for the habit.
            - update_expiry (datetime.datetime): The date when the user's habit streak will expire if not updated.
            - streak (int): The number of consecutive days the user has checked in for the habit.
            - control_interval (int): The number of days for each monitoring interval for the habit.
            - status (str): The status of the active habit.
        """

        # Establish connection to the database
        self.connect()

        # Query for returning all active habits from the user.
        query = """SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        WHERE active_user_habits.user_ID = %s AND active_user_habits.status != 'deleted';
                """
        # Execute constructed query
        self.cursor.execute(query, (user_ID,))
        active_habits = self.cursor.fetchall()

        # Commit changes to the database
        self.connection.commit()
        
        # Close cursor and connection
        self.cursor.close()
        self.connection.close()

        # Disconnect function
        self.disconnect()

        # Return loist with active habits
        return active_habits
    
    def get_global_active_habits(self,interval_ID):
        """
        Returns all stored active habits across all users with a given monitoring interval.
        
        Args:
            interval_ID (int): The ID of the monitoring interval for the active habits to be retrieved.
        
        Returns:
            A list of tuples, where each tuple represents an active habit and contains the following values:
            - active_habits_ID (int): The ID of the active habit.
            - habit_name (str): The name of the habit.
            - starting_date (datetime.datetime): The date when the user started the habit.
            - last_check (datetime.datetime): The date when the user last checked in for the habit.
            - update_expiry (datetime.datetime): The date when the user's habit streak will expire if not updated.
            - streak (int): The number of consecutive days the user has checked in for the habit.
            - control_interval (int): The number of days for each monitoring interval for the habit.
            - status (str): The status of the active habit.
            - username (str): The username of the user associated with the active habit.
        """
        # Connect to database
        self.connect()

        # Query for returning all active habits from the user.
        query = f"""SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status, user_table.username
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        INNER JOIN user_table ON active_user_habits.user_ID = user_table.user_ID
                        WHERE active_user_habits.interval_ID = {interval_ID}   
                        ORDER BY active_user_habits.streak DESC;
                """
        
        # Execute constructed query
        self.cursor.execute(query)
        active_habits = self.cursor.fetchall()

        # Commit changes to the database
        self.connection.commit()
        
        # Close cursor and connection
        self.cursor.close()
        self.connection.close()

        # Disconnect function
        self.disconnect()
        # Return list
        return active_habits
    
    def get_all_active_habits(self, user_ID):
        """
        Returns all stored active habits of a user.
        
        Args:
            user_ID (int): The user ID for the user whose active habits are to be retrieved.
        
        Returns:
            A list of tuples, where each tuple represents an active habit and contains the following values:
            - active_habits_ID (int): The ID of the active habit.
            - habit_name (str): The name of the habit.
            - starting_date (datetime.datetime): The date when the user started the habit.
            - last_check (datetime.datetime): The date when the user last checked in for the habit.
            - update_expiry (datetime.datetime): The date when the user's habit streak will expire if not updated.
            - streak (int): The number of consecutive days the user has checked in for the habit.
            - control_interval (int): The number of days for each monitoring interval for the habit.
            - status (str): The status of the active habit.
            - goal_streak (int): The user's goal streak for the habit.
        """
        # Establish connection to the database
        self.connect()

        # Query for returning all active habits from the user.
        query = """SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status, active_user_habits.goal_streak
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        WHERE active_user_habits.user_ID = %s
                        ORDER BY active_user_habits.streak DESC;
                """
  
        self.cursor.execute(query, (user_ID,))
        active_habits = self.cursor.fetchall()

        # Commit changes to the database
        self.connection.commit()
        
        # Close cursor and connection
        self.cursor.close()
        self.connection.close()

        # Disconnect function
        self.disconnect()

        # Return all active habits as a list of tuples
        return active_habits

    def get_active_habit_ID(self, user_ID, habit_ID, status):
        """
        Returns the active_habit_ID for a specific active habit of a user.
        
        Args:
            user_ID (int): The user ID for the user whose active habit ID is to be retrieved.
            habit_ID (int): The habit ID for the habit whose active habit ID is to be retrieved.
            status (str): The status of the active habit for which the ID is to be retrieved.
        
        Returns:
            An integer representing the ID of the active habit.
        """

        # Connect to db.
        self.connect()

        # Query
        query = f""" SELECT active_habits_ID FROM active_user_habits
                    WHERE user_ID = {user_ID} AND habit_ID = {habit_ID} AND status = "{status}";
        """ 
        self.cursor.execute(query)
        active_habit_ID = self.cursor.fetchone()

        # Commit changes to the database
        self.connection.commit()
        self.disconnect()
        if len(active_habit_ID) > 1:
            print("Too many possible habits")
        elif len(active_habit_ID) < 1:
            print("No habit found")
        else:
            # store the first value from the list
            result = int(active_habit_ID[0])
            return result
    
    # Function to get the current streak for a active_habit
    def get_streak(self, active_habits_ID):
        """
        Returns the current streak for a specific active habit from a user.
    
        Args:
            active_habits_ID (int): The ID of the active habit.
    
        Returns:
            An integer representing the current streak for the active habit.
        """

        # Establish connection
        self.connect()

        # Construct query
        query = f"""SELECT streak FROM active_user_habits
                    WHERE active_habits_ID = {active_habits_ID}"""
        
        # Execute query
        self.cursor.execute(query)

        # Get the streak
        streak = self.cursor.fetchone()

        # Commit changes to the database
        self.connection.commit()

        # Disconnect function
        self.disconnect()

        # Check if one value was retrieved
        if len(streak) > 1:
            print("Too many possible habits")
        elif len(streak) < 1:
            print("No habit found")
        else:
            # store the first value from the list
            result = int(streak[0])

            # Return the current streak
            return result
         
    def delete_habit(self, habit_ID):
        """
        Deletes a habit from the habits table in the database.
        
        Args:
            habit_ID (int): The ID of the habit to be deleted.
        """
        
        # Establish connection
        self.connect()

        # Query for deleting a habit from the habits table using the habit_ID
        query = f"""DELETE FROM habits WHERE habit_ID = {habit_ID};"""

        # Execute query
        self.cursor.execute(query)

        # Commit changes to the database
        self.connection.commit()
        
        # Disconnect function
        self.disconnect()

    def update_value(self, table_name, data, column1, column2, value1, value2, join_table = None):
        """
        Updates a value in a  database table with the information of two columns.
        
        Args:
            table_name (str): The name of the table to update.
            data (dict): A dictionary with the column names as keys and the new values as values.
            column1 (str): The name of the first column to use for updating.
            column2 (str): The name of the second column to use for updating.
            value1 (any): The value of the first column to use for updating.
            value2 (any): The value of the second column to use for updating.
            join_table (str, optional): The name of the table to join. Defaults to None.
        """
        # Connect to db
        self.connect()      
        
        # Set string for the sql query
        set_str = ", ".join([f"{col_name} = '{col_value}'" for col_name, col_value in data.items()])
        table_join = f" INNER JOIN {join_table} ON {table_name}"
        
        # Execute the query for updating values
        self.cursor.execute(f"UPDATE {table_name} SET {set_str} WHERE {table_name}.{column1} = '{value1}' AND {table_name}.{column2} = '{value2}';")
        
        self.connection.commit()
        print(f"Data updated successfully")
        self.disconnect()  

    def get_user_categories(self, user_ID):
        """
        Retrieves all categories stored for a given user from the database.

        Args:
        - user_ID (int): The unique identifier for the user.

        Returns:
        - categories (list of tuples): A list of tuples where each tuple represents a category. The tuple contains the following information:
            - category_ID (int): The unique identifier for the category.
            - category_name (str): The name of the category.
            - description (str): The description of the category.
            - creation_date (str): The date when the category was created.
        """
        # Connect to db
        self.connect()

        query = """SELECT category.category_ID, category.category_name, category.description, category.creation_date
	                    FROM category  
                        WHERE category.user_ID = %s OR category.user_ID = 99;
                """    
        self.cursor.execute(query, (user_ID,))
        categories = self.cursor.fetchall()

        # Commit changes to the database
        self.connection.commit()
        
        # Disconnect function
        self.disconnect()

        return categories
    
    # Function for querying for all stored categories of a user (only catgeory name)
    def get_user_categories_name(self, user_ID):
        """
        Retrieves the names of all categories stored for a given user from the database.

        Args:
        - user_ID (int): The unique identifier for the user.

        Returns:
        - categories (list of tuples): A list of tuples where each tuple represents a category name (str). The tuple contains the following information:
        """
        
        # Connect to db
        self.connect()

        query = """SELECT category.category_name
	                    FROM category  
                        WHERE category.user_ID = %s OR category.user_ID = 99;      
                """    
        self.cursor.execute(query, (user_ID,))
        categories = self.cursor.fetchall()

        # Commit changes to the database
        self.connection.commit()
        
        # Disconnect function
        self.disconnect()

        return categories

    def get_category_ID(self, category_name, user_ID):
        """
        Retrieves the unique identifier for a category given its name and the unique identifier of its owner.

        Args:
        - category_name (str): The name of the category.
        - user_ID (int): The unique identifier for the user.

        Returns:
        - category_ID (int): The unique identifier for the category.
        """
        
        # Connect to db
        self.connect()

        table = "category"
        column = "category_name"

        # Query for returning user_ID
        sql = f"SELECT category_ID FROM {table} WHERE {column} = '{category_name}' AND (user_ID = {user_ID} OR user_ID = 99);"

        # Execute Query
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        # Print out the results
        if len(result) > 0:
            category_ID = result[0]

            # Commit changes to the database
            self.connection.commit()
            self.disconnect()
            return category_ID
        # Print category not found if result not fond
        else:
            print("Category not found.")
            # Commit changes to the database
            self.connection.commit()
            self.disconnect()
    
    def delete_category(self, category_ID):
        """Delete a category from a specific user in the database.
        
        Args:
            category_ID (int): The ID of the category to delete.
            
        Returns:
            None
        """
        
        # Connect to db
        self.connect()

        # Query for deleting a category from the category table using the category_ID
        query = f"""DELETE FROM category WHERE category_ID = {category_ID};"""

        # Execute query
        self.cursor.execute(query)

        # Commit changes to the database
        self.connection.commit()
        
        # Disconnect function
        self.disconnect()

    def execute_query(self, query):
        """Execute a SQL query.
    
        Args:
            query (str): The SQL query to execute.
            
        Returns:
            results (tuple): The results of the SQL query.
        """
        # Connect to db
        self.connect()
        self.query = query

        # Execute query
        self.cursor.execute(query)
        results = self.cursor.fetchone()

        # Commit changes to the database
        self.connection.commit()
        
        # Disconnect function
        self.disconnect()

        return results
  






# db = MySQLDatabase("localhost","root","Mannheim", "zepp")
# query = "SELECT username FROM user_table WHERE user_ID = 1;"
# habits = db.execute_query(query)

# query = "SELECT username FROM user_table WHERE user_ID = 2;"
# habits1 = db.execute_query(query)


# print(habits1)
# print(habits)
# db.create_table()
# db.connect()



# db.create_database_tables("lulu")







#insert = "INSERT INTO user_table (user_ID, first_name, last_name, username, password, email, phone_number, created_time, last_update) VALUES (67, 'Heinz', 'Huber', 'lui', 'hubinho', 'heinz.huber@web.de', '01768907654', '2023-03-15 10:00:00', '2023-03-20 11:05:00');"
#db.cursor.execute(insert)
# db.connection.commit()

# #sys_habits = db.get_user_habits(99)
# all_active = db.get_global_active_habits(3)
# print(all_active)


#db.connect()
# db.initialize_database("test")
# result = db.get_all_active_habits(2)
# print(result)
# db.get_habit_ID(2,'Soccer')

# db.get_category_ID("Meditation",99)

# #db.delete_habit(2)
# db.get_category_ID("sport",2)



  

    


    








