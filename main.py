import tkinter as tk
from tkinter import messagebox
# from tkinter import ttk
# from tkinter import simpledialog
# import tkcalendar
import mysql.connector
# from mysql.connector.errors import Error
from database import MySQLDatabase
from user import User
from main_screen import Main_screen
# from habit import Habit
# from active_user_habits import ActiveUserHabit
# from category import Category
import os
# from datetime import datetime as dt
# from datetime import timedelta
# import pandas as pd
# import matplotlib.pyplot as plt


"""
This file contains the main classes and functions for the Habit Tracker application.

Classes:
- database_connection_screen: The first screen of the Habit Tracker where the user enters database credentials.
- login_screen: The screen where the user logs in to the Habit Tracker and creates a new account.
"""

class database_connection_screen(tk.Tk):
    """The first screen of the Habit Tracker where the user enters database credentials for MySQL Database.

    This screen contains several labels and input fields, including:

        - A label welcoming the user to the screen.
        - A label indicating the 'Host' input field.
        - An input field for the user to enter the host of their MySQL database.
        - A label indicating the 'User' input field.
        - An input field for the user to enter the username of their MySQL database.
        - A label indicating the 'Password' input field.
        - An input field for the user to enter the password of their MySQL database.
        - A label indicating the 'Database' input field.
        - An input field for the user to enter the name of their MySQL database.
        - A button that triggers the `confirm_values` function.

    Methods:
        confirm_values: Validates the user's input values, creates the database if it doesn't already exist, and stores
                        the credentials in an environmental variable for later use by the Habit Tracker.
    """
    def __init__(self):
        super().__init__()
        self.title("Database Connection")
        self.geometry("500x350")

        global entry_host, entry_user, entry_password, entry_database
    
        # Create the welcome label
        self.welcome_label = tk.Label(self, text="Welcome! Please enter your database connection information:")
        self.welcome_label.pack()
        
        # Create the host label and entry widget
        self.host_label = tk.Label(self, text="Host:")
        self.host_label.pack()
        self.entry_host = tk.Entry(self)
        self.entry_host.pack()

        # Create the port label and entry widget
        self.port_label = tk.Label(self, text="Port:")
        self.port_label.pack()
        self.entry_port = tk.Entry(self)
        self.entry_port.pack()
        
        # Create the user label and entry widget
        self.user_label = tk.Label(self, text="User:")
        self.user_label.pack()
        self.entry_user = tk.Entry(self)
        self.entry_user.pack() 

        # Create the password label and entry widget
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()
        
        # Create the database label and entry widget
        self.database_label = tk.Label(self, text="Database:")
        self.database_label.pack()
        self.entry_database = tk.Entry(self)
        self.entry_database.pack()

        # Create the confirm button
        self.confirm_button = tk.Button(self, text="Confirm", command = self.confirm_values)
        self.confirm_button.pack()                      
    
    # Function for confrim button
    def confirm_values(self):
        """
        Handle the confirmation button click in the database connection screen.

        Retrieve the values entered into the host, user, password, and database entry fields, and use them to create a new
        MySQLDatabase object using the `host`, `user`, and `password` parameters. Call the `create_database` method of the
        new object, which creates a new database with the name specified in the `database` entry field if it does not already
        exist.

        Test the database connection using a `try` block. If the connection is successful, store the database credentials in
        an environmental variable for use in the habit tracker. Finally, close the database connection, destroy the current
        window, and open the login screen.

        Raises:
            mysql.connector.Error: If there is an error connecting to the database.

        Returns:
            None
        """  
        host = self.entry_host.get()
        port = self.entry_port.get()
        user = self.entry_user.get()
        password = self.entry_password.get()
        database = self.entry_database.get()

        db = MySQLDatabase(host,user,password,port)
        db.create_database(database)

        try:
            db = mysql.connector.connect(host=host, user=user, password=password, port=port, database=database)
            print("Connection successful!") # Test if database connection is successfull
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
        finally:
            if db:
                self.var_string = f"{host},{user},{password},{port},{database}" # Concatenate database variables into a single string
                os.environ["Database_Variables"] = self.var_string       # Set environment variable for later database connection
                db.disconnect()
                self.destroy() 
                self.open_next_window() # Calls function for opening the Login Screen window 
    
    # After successfully creating a new Database the next window (Login Screen) opens
    def open_next_window(self):
        global login_screen
        login_screen = login_screen()
        login_screen.mainloop()


class login_screen(tk.Tk):  
    """The Login Screen class contains the window for the user login. A user can either login to the habit tracker
    using username and password or create a new account using the registration button
    """
    def __init__(self):
        super().__init__()
        self.title("Login/Registration Habit Tracker")
        self.geometry("250x350")
        
        # Retrieve environment variable
        retrieved_var_string = os.getenv("Database_Variables")
        # Split the string back into separate variables
        retrieved_vars = retrieved_var_string.split(",")
        self.db = MySQLDatabase(retrieved_vars[0],retrieved_vars[1],retrieved_vars[2], retrieved_vars[3], retrieved_vars[4])

        tk.Label(text = "Login/Registration Habit Tracker", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
        tk.Label(text = "").pack()
        tk.Button(text = "Login", height = "2", width = "30", command = self.login).pack()
        tk.Label(text = "").pack()
        tk.Button(text = "Register", height = "2", width = "30", command = self.register).pack()
    
    def register(self):
        """
        Opens a popup window where new users can create an account. The 'Register' button
        calls the function save_registration() which saves the input data in the database.
        """
        
        self.popup = tk.Toplevel()
        self.popup.geometry("300x500")
        self.popup.title("Registration")
        self.popup.grab_set() # Disables interaction with parent window

        self.login_label = tk.Label(self.popup, text="Please enter your details below:")
        self.login_label.pack()
        tk.Label(self.popup, text="").pack()

        # Create Label and Entry for first_name
        self.first_name_label = tk.Label(self.popup, text="First Name")
        self.first_name_label.pack()
        self.entry_first_name = tk.Entry(self.popup)
        self.entry_first_name.pack()

        # Create Label and Entry for last_name
        self.last_name_label = tk.Label(self.popup, text="Last Name")
        self.last_name_label.pack()
        self.entry_last_name = tk.Entry(self.popup)
        self.entry_last_name.pack()

        # Create Label and Entry for username
        self.username_label = tk.Label(self.popup, text="Username")
        self.username_label.pack()
        self.entry_username = tk.Entry(self.popup)
        self.entry_username.pack()

        # Create Label and Entry for password
        self.password_label = tk.Label(self.popup, text="Password")
        self.password_label.pack()
        self.entry_password = tk.Entry(self.popup)
        self.entry_password.pack()

        # Create Label and Entry for email
        self.email_label = tk.Label(self.popup, text="Email")
        self.email_label.pack()
        self.entry_email = tk.Entry(self.popup)
        self.entry_email.pack()

        # Create Label and Entry for Phone_number
        self.phone_number_label = tk.Label(self.popup, text="Phone_number")
        self.phone_number_label.pack()
        self.entry_phone_number = tk.Entry(self.popup)
        self.entry_phone_number.pack()

        tk.Button(self.popup, text="Register", command = self.save_registration, width=10, height=1).pack()

        self.popup.wait_window()  # Wait for popup window to be destroyed

    def save_registration(self):
        """
        Stores the input user data in the database and closes the popup window.
        """ 

        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        phone_number = self.entry_phone_number.get()
        
        # Check if any of the variables are empty. If so user cannot register
        if not all([first_name, last_name, username, password, email, phone_number]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Check if the phone number entered contains only numbers
        if not phone_number.isnumeric():
            messagebox.showerror("Error", "Phone number must contain only digits")
            return      
        
        # Check if the email address contains a @. If not user cannot register.
        if "@" not in email:
            messagebox.showerror("Error", "Your email address doesn't contain a @")
            return

        # Use User class to create a new user instance
        new_user = User(first_name,last_name,username, password, email, phone_number)
        data = {'username': username, 'first_name': first_name, 'last_name': last_name, 'username': username, 'password': password, 'email': email, 'phone_number': phone_number, 'created_time': new_user.created_time, 'last_update': new_user.last_update }
        
        try:
            # If everything is correct a new user is saved in the database
            self.db.insert_data("user_table", data)
            messagebox.showinfo("Success", "User: {} successfully registered".format(username))
            self.popup.destroy()
        
        except mysql.connector.IntegrityError as e:
            # Catch the exception thrown if the username already exists
            messagebox.showerror("Error", "An error occurred: {}".format(str(e)))
            print("MySQL error: {}".format(e))
            self.popup.destroy()
               
    def login(self):
        """
        Opens a toplevel login screen where a user can enter username and password, and confirm it with a login button.
        If the login is successful, sets environment variables for the active user credentials and opens the main screen of the Habit Tracker.
        """
        
        self.popup = tk.Toplevel()
        self.popup.geometry("300x250")
        self.popup.title("Login")
        self.popup.grab_set() # Disables interaction with parent window

        username = tk.StringVar()
        password = tk.StringVar()

        # Create Label and Entry for username
        self.username_label = tk.Label(self.popup, text = "Username")
        self.username_label.pack()
        self.entry_username = tk.Entry(self.popup)
        self.entry_username.pack()

        # Create Label and Entry for password
        self.password_label = tk.Label(self.popup, text="Password")
        self.password_label.pack()
        self.entry_password = tk.Entry(self.popup)
        self.entry_password.pack()

        # Button for calling login_process function
        tk.Button(self.popup, text = "Login", command = self.login_process, width = 10, height = 1).pack()
        
        # Wait for popup window to be destroyed     
        self.popup.wait_window()

    def login_process(self):
        """
        Processes the user inputs from the login screen, checks if the user exists in the database, and if so, sets environment variables for the active user credentials and opens the main screen of the Habit Tracker.
        If the user inputs are incorrect, displays an error message.
        """
        # Get the username and password from the user inputs
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Create query for checking the database for the user
        query = "SELECT * FROM user_table WHERE username = %s AND password = %s"
        self.db.connect()
        self.db.cursor.execute(query, (username, password))
        user = self.db.cursor.fetchone()
        
        if user is not None:
            # Login successfull, open main window.
            messagebox.showinfo("Success", "Hello {} you can now enjoy the Habit Tracker! Have fun and stay active!".format(username))
            self.user_string = f"{username},{password}"           # Concatenate user variables into a single string
            os.environ["User_Variables"] = self.user_string       # Set environment variable in dictionary for storing the active user credentials
            
            # Store the Primary Key of the active User as an environment variable for later use
            self.active_user_ID = self.db.get_userID(username)    
            os.environ["active_user_ID"] = str(self.active_user_ID)
            
            # disconnet from database, close popup and login screen and open the main window of the Habit Tracker
            self.db.disconnect()
            #print(os.getenv("active_user_ID"))
            self.popup.destroy()
            login_screen.destroy()
            self.open_main_screen()

        else:
            # Wrong user/password
            messagebox.showerror("Error", "Wrong Username or Password! Please try again.")
            self.popup.destroy()
            self.db.disconnect()
    
    # Opens the window for the main_screen class
    def open_main_screen(self):
        global Main_screen
        main_screen = Main_screen()
        main_screen.mainloop()

if __name__ == '__main__':
    window = database_connection_screen()
    window.mainloop()














