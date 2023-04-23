import mysql.connector
import time
from tkinter import messagebox

class MySQLDatabase:
    def __init__(self, host, user, password, database = None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    
    # Connect to the MySQL database
    def connect(self):
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
        self.cursor = self.connection.cursor()

    # Disconnects from the database
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
        if self.cursor is not None:
            self.cursor.close()

    
    # Creates a MySQL Database with name = new_database if a database doesn't already exist with this name. When creating a new database it also calls the intitialize database function which creates tables and stores example data within the database.
    def create_database(self,new_database):
        self.connect()
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_database}")
        self.database = new_database
        if self.cursor.rowcount == 1:
            self.initialize_database(self.database) # Call database initialization function if a new database was created
            messagebox.showinfo("Success", "Database created. You can go on and login/register.")
        self.disconnect()

    # Initializes creating all necessary tables and sample data
    def initialize_database(self,database):
        # Read the contents of the file that contains the SQL statements
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
                #print("Connection before connect():", self.connection)
                self.connect()
                #print("Connection after connect():", self.connection)
                query = insert
                self.cursor.execute(query)
                self.connection.commit()
                rows_affected = self.cursor.rowcount
                if rows_affected == 0:
                    print("No rows were inserted into the database.")
                else:
                    print(f"{rows_affected} rows were inserted into the database.")
                #self.cursor.close()
                #print(query)
                print(f"Insert {counter} executed, {query}")
                time.sleep(0.15)
            except Exception as e:
                print("An error occurred:", e)


    # Creates a new table in the database if its not already existing
    def create_table(self, table_name, *columns):
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
    
    # Deletes a table from the database
    def delete_table(self, table_name):
        self.connect()
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Table '{table_name}' deleted successfully")
        self.disconnect()
 
 
    # Inserts Values into tables  
    def insert_data(self, table_name, data):
        self.connect()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data.values()))
        values = tuple(None if v == '' else v for v in data.values()) # set None for empty string values in dict
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        print(f"{self.cursor.rowcount} row(s) inserted into {table_name}.")      

    
    
    """
    The data variable has to be defined as a dictionary first. Updates data of a given table. 
    Data has to be a dictionary. Object is the primary key name without _ID. ID is the int value of the unique primary key.
 
    """
    def update_data(self, table_name, data, object, ID):
        self.connect()
        # Construct name of the primary key for where clause
        primary_key = f"{object}_ID"
        
        # Set string for the sql query
        set_str = ", ".join([f"{col_name} = '{col_value}'" for col_name, col_value in data.items()])
        
        # Execute the query for updating values
        self.cursor.execute(f"UPDATE {table_name} SET {set_str} WHERE {primary_key} = {ID} ")
        self.connection.commit()
        #print(f"Data updated successfully")
        self.disconnect()



    # Function to check wether a value exists in a table,column
    def  check_value(self, searched_value, table, column, value):
        #establish connection with the database
        self.connect()  
        # query  
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
    
    # Function for querying the database for all user credentials by using the Primary Key (user_ID) and returning a dictionary
    def get_user_credentials(self,user_ID):

        self.connect()

        table = "user_table"
        column_names = ["user_ID", "username", "first_name", "last_name", "password", "email", "phone_number", "created_time", "last_update"]
        
        # Construct the SQL query
        query = f"SELECT {', '.join(column_names)} FROM {table} WHERE user_ID = %s"
        
        # Execute the query and fetch the results
        cursor = self.connection.cursor()
        cursor.execute(query, (user_ID,))
        result = cursor.fetchone()
        
        # Store the results in a dictionary
        if result:
            result_dict = dict(zip(column_names, result))
        else:
            result_dict = {}
        
        cursor.close()
        self.connection.close()
        
        return result_dict


    # Function to give back the unique user_ID for a username
    def  get_userID(self, username):
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
   

   # Function for querying for all stored habits of a user
    def get_user_habits(self, user_ID):
        self.connect()
        cursor = self.connection.cursor()
        # Query for returning all habits from the user plus the predefined system user habits. The Systemuser has the user_ID 99
        query = """SELECT habits.habit_ID, habits.habit_name, habits.description, habits.creation_date, category.category_name
	                    FROM habits  
                        INNER JOIN category ON habits.category_ID = category.category_ID
                        WHERE habits.user_ID = %s OR habits.user_ID = 99;                
                """    
        cursor.execute(query, (user_ID,))
        habits = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return habits
    
    # Function to get a habit_ID by using the habit_name and user_ID
    def get_habit_ID(self, user_ID, habit_name):
        self.connect()
        # Information about user and habit
        self.user_ID = user_ID
        self.habit_name = habit_name
        
        table_name = 'habits'
        cursor = self.connection.cursor()
        # Query for returning the habit_ID 
        query = f'''SELECT active_user_habits.habit_ID FROM active_user_habits
                    INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                    WHERE habits.habit_name = '{habit_name}' AND (habits.user_ID = {user_ID} OR habits.user_ID = 99)
                '''
        cursor.execute(query)
        habit_ID = cursor.fetchone()
        #print(habit_ID)
        return habit_ID
    

    # Function for querying for all stored active habits of a user. The active habits in the table with the status deleted are excluded.
    def get_active_habits(self, user_ID):
        self.connect()
        cursor = self.connection.cursor()
        # Query for returning all active habits from the user.
        query = """SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        WHERE active_user_habits.user_ID = %s AND active_user_habits.status != 'deleted';
                """
        #print(query)    
        cursor.execute(query, (user_ID,))
        active_habits = cursor.fetchall()
        #print(active_habits)
        cursor.close()
        self.connection.close()
        return active_habits
    
    def get_global_active_habits(self,interval_ID):
        self.connect()
        cursor = self.connection.cursor()
        # Query for returning all active habits from the user.
        query = f"""SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status, user_table.username
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        INNER JOIN user_table ON active_user_habits.user_ID = user_table.user_ID
                        WHERE active_user_habits.interval_ID = {interval_ID}   
                        ORDER BY active_user_habits.streak DESC;
                """
        #print(query)    
        cursor.execute(query)
        active_habits = cursor.fetchall()
        #print(active_habits)
        cursor.close()
        self.connection.close()
        return active_habits
    
    def get_all_active_habits(self, user_ID):
        self.connect()
        cursor = self.connection.cursor()
        # Query for returning all active habits from the user.
        query = """SELECT active_user_habits.active_habits_ID, habits.habit_name, active_user_habits.starting_date, active_user_habits.last_check, active_user_habits.update_expiry, active_user_habits.streak, monitoring_interval.control_interval, active_user_habits.status, active_user_habits.goal_streak
	                    FROM active_user_habits  
                        INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        INNER JOIN monitoring_interval ON active_user_habits.interval_ID = monitoring_interval.interval_ID
                        WHERE active_user_habits.user_ID = %s
                        ORDER BY active_user_habits.streak DESC;
                """
        #print(query)    
        cursor.execute(query, (user_ID,))
        active_habits = cursor.fetchall()
        #print(active_habits)
        cursor.close()
        self.connection.close()
        return active_habits

    # Function for querying for the active_habit_ID for a specific activce habit from a user
    def get_active_habit_ID(self, user_ID, habit_ID, status):
        self.connect()
        cursor = self.connection.cursor()
        # Query
        query = f""" SELECT active_habits_ID FROM active_user_habits
                    WHERE user_ID = {user_ID} AND habit_ID = {habit_ID} AND status = "{status}";
        """ 
        cursor.execute(query)
        active_habit_ID = cursor.fetchone()
        cursor.close()
        self.connection.close()
        if len(active_habit_ID) > 1:
            print("Too many possible habits")
        elif len(active_habit_ID) < 1:
            print("No habit found")
        else:
            # store the first value from the list
            result = int(active_habit_ID[0])
            #print(query)
            return result
    
    # Function to get the current streak for a active_habit
    def get_streak(self, active_habits_ID):
        self.connect()
        cursor = self.connection.cursor()

        query = f"""SELECT streak FROM active_user_habits
                    WHERE active_habits_ID = {active_habits_ID}"""
        cursor.execute(query)
        streak = cursor.fetchone()
        cursor.close()
        self.connection.close()
        if len(streak) > 1:
            print("Too many possible habits")
        elif len(streak) < 1:
            print("No habit found")
        else:
            # store the first value from the list
            result = int(streak[0])
            #print(query)
            return result
         
    
    # Function for deleting a habit from a specific user in the database
    def delete_habit(self, habit_ID):
        self.connect()
        cursor = self.connection.cursor()
        # Query for deleting a habit from the habits table using the habit_ID
        query = f"""DELETE FROM habits WHERE habit_ID = {habit_ID};
                COMMIT;"""
        #print(query)
        cursor.execute(query,multi=True)
        cursor.close()
        self.connection.close()

    # Update a value in a table with the information of two columns
    def update_value(self, table_name, data, column1, column2, value1, value2, join_table = None):
        self.connect()      
        
        # Set string for the sql query
        set_str = ", ".join([f"{col_name} = '{col_value}'" for col_name, col_value in data.items()])
        table_join = f" INNER JOIN {join_table} ON {table_name}"
        # Execute the query for updating values
        #self.cursor.execute(f"UPDATE {table_name} SET {set_str} WHERE {table_name}.{column1} = {value1} AND {table_name}.{column2} = {value2}")
        print(f"UPDATE {table_name} {table_join} SET {set_str} WHERE {table_name}.{column1} = {value1} AND {table_name}.{column2} = {value2}")
        self.connection.commit()
        print(f"Data updated successfully")
        self.disconnect()  


   # Function for querying for all stored categories of a user (only catgeory name)
    def get_user_categories(self, user_ID):
        self.connect()
        cursor = self.connection.cursor()
        #query = "SELECT * FROM habits WHERE user_ID = %s"
        query = """SELECT category.category_ID, category.category_name, category.description, category.creation_date
	                    FROM category  
                        WHERE category.user_ID = %s OR category.user_ID = 99;
                """    
        cursor.execute(query, (user_ID,))
        categories = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return categories
    
    # Function for querying for all stored categories of a user (only catgeory name)
    def get_user_categories_name(self, user_ID):
        self.connect()
        cursor = self.connection.cursor()
        #query = "SELECT * FROM habits WHERE user_ID = %s"
        query = """SELECT category.category_name
	                    FROM category  
                        WHERE category.user_ID = %s OR category.user_ID = 99;      
                
                """    
        cursor.execute(query, (user_ID,))
        categories = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return categories
    
     # Function to give back the unique catgeory_ID for a category_name and a unique user_ID
    def get_category_ID(self, category_name, user_ID):
        self.connect()

        table = "category"
        column = "category_name"

        # query for returning user_ID
        sql = f"SELECT category_ID FROM {table} WHERE {column} = '{category_name}' AND (user_ID = {user_ID} OR user_ID = 99);"
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        # Print out the results
        if len(result) > 0:
            category_ID = result[0]
            #print(category_ID)
            self.disconnect()
            return category_ID
        # 
        else:
            print("Category not found.")
            self.disconnect()
    
    # Function for deleting a category from a specific user in the database
    def delete_category(self, category_ID):
        self.connect()
        cursor = self.connection.cursor()
        # Query for deleting a category from the category table using the category_ID
        query = f"""DELETE FROM category WHERE category_ID = {category_ID};"""
        #print(query)
        cursor.execute(query)
        cursor.close()
        self.connection.close()

    # Function for executing a query
    def execute_query(self, query):
        self.connect()
        self.query = query
        self.cursor.execute(query)
        results = self.cursor.fetchone()
        self.connection.close()
        return results
    
    def create_database_tables(self,database):
    # Read the contents of the file that contains the SQL statements
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

    


        










# db = MySQLDatabase("localhost","root","Mannheim","lulu")
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



  

    


    








