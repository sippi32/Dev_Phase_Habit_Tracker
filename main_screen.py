import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
import tkcalendar
import mysql.connector
from mysql.connector.errors import Error
from database import MySQLDatabase
from user import User
from habit import Habit
from active_user_habits import ActiveUserHabit
from category import Category
import os
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt

class Main_screen(tk.Tk):
    """A class representing the main screen of the habit tracker GUI, containing all its functionalities.
    
    Attributes:
    - db: A MySQLDatabase object for connecting to the database
    - username: A string representing the active user's username
    - password: A string representing the active user's password
    - user_ID: An integer representing the active user's ID in the database

    Methods:
    - open_myHabits: Opens the MyHabits screen where the user can create and delete habits
    - open_myCategories: Opens the MyCategories screen where the user can create and delete categories
    - open_analyze_myhabits: Opens the Activate Habits screen where the user can set predefined habits to active
    - update_profile: Opens the Update Profile screen where the user can update their profile information
    - open_highscores: Opens the Highscores screen where the user can see their own and public streaks and highscores
    - close_application: Closes the Habit Tracker application
    - check_habit: Marks an active habit as completed and updates the table accordingly
    - reactivate_active_habit: Reactivates an active habit where to user failed to check in time and updates the table accordingly
    - delete_active_habit: Deletes an active habit and updates the table accordingly
    - update_active_habits_table: Updates the table of active habits with current data from the database
    - update_time: Updates the time label on the screen with the current time
    """

    def __init__(self, isTest=False):
        if not isTest:
            super().__init__()
            self.title("Habit Tracker")
            self.geometry("800x700")
            self.resizable(False,False)

            # Retrieve environment variable for the database connection
            retrieved_var_string = os.getenv("Database_Variables")
            # Split the string back into separate variables
            retrieved_vars = retrieved_var_string.split(",")
            self.db = MySQLDatabase(retrieved_vars[0],retrieved_vars[1],retrieved_vars[2], retrieved_vars[3])

            # Retrieve environment variable for the active user information
            retrieved_var_string = os.getenv("User_Variables")
            # Split the string back into separate variables
            retrieved_vars = retrieved_var_string.split(",")
            
            # Store the retrieved information about the current logged in user in the corresponding variables
            self.username = retrieved_vars[0]
            self.password = retrieved_vars [1]
            self.user_ID = self.db.get_userID(self.username)

            # Button for opening the MyHabits Screen where user can see and define own habits
            Button_1 = tk.Button(text="MyHabits",  width = 22, height=3, font = ("Arial",12, "bold"),command = self.open_myHabits)
            Button_1.place(x = 5, y = 60)

            # Button for opening the MyCategories Screen where user can see and define own categories
            Button_2 = tk.Button(text = "MyCategories", font = ("Arial",12, "bold"), width = 22, height=3, command = self.open_myCategories)
            Button_2.place(x = 5, y = 160)
            
            # Button for opening the Activate Habits Screen. In this screen a user is able to set predefined habits to active.
            Button_3 = tk.Button(text = "Analyze MyHabits", font = ("Arial",12, "bold"), width = 22, height=3, command = self.open_analyze_myhabits)
            Button_3.place(x = 5, y = 260)    
            
            # Button for opening the Update Profile Screen.
            Button_5 = tk.Button(text = "Update Profile", font = ("Arial",12, "bold"), width = 22, height=3, command = self.update_profile)
            Button_5.place(x = 5, y = 460)
            
            # Button for opening the Analyze Screen. In this screen a user can see his own and public streaks and highscores
            Button_6 = tk.Button(text = "Highscores", font = ("Arial",12, "bold"), width = 22, height=3, command = self.open_highscores)
            Button_6.place(x = 5, y = 560)  
            
            # Exit Button. Closes the Habit Tracker.
            Button_7 = tk.Button(text = "Exit", height = "1", width = "10", bg = "red", command = self.close_application)
            Button_7.place(relx = 1, rely = 1, anchor = 'se')

            # Button for checking off a active habit.
            Button_8 = tk.Button(text = "Check Habit", font = ("Arial",8, "bold"), width = 15, height=2, command = self.check_habit)
            Button_8.place(x = 280, y = 350)

            # Button for reactivating a habit if the streak was lost.
            Button_9 = tk.Button(text = "Reactivate Habit", font = ("Arial",8, "bold"), width = 15, height=2, command = self.reactivate_active_habit)
            Button_9.place(x = 405, y = 350)

            # Button for deleting a active habit.
            Button_10 = tk.Button(text = "Delete Active Habit", font = ("Arial",8, "bold"), width = 15, height=2, command = self.delete_active_habit)
            Button_10.place(x = 525, y = 350)

            # Button for updating whole table.
            Button_11 = tk.Button(text = "Update Table", font = ("Arial",8, "bold"), width = 15, height=2, command = self.update_active_habits_table)
            Button_11.place(x = 645, y = 350)

            # Create a label to show the current time on screen
            self.time_label = tk.Label(self, text="")
            self.time_label.place(x = 0, y = 680)
            self.update_time()

            '''
            The following code creates a ttk treeview widget. The Table shows all active user habits on the right side 
            of the main screen window. The user can see the remaining time and the deadline for each active habit. Also
            the user can check off a habit and set the remaining time back. Depending on the choosen monitoring interval.
            '''

            # Create Treeview to show active habits and enable user to check off a habit
            self.active_habits_tree = ttk.Treeview(self)
            self.active_habits_tree.place(x=280, y=100)

            # Create a label widget for the title
            title_label = tk.Label(self, text="Active Habits", font=("Arial", 16, "bold"))
            title_label.place(x=280, y=70)
        
            # Define Columns
            self.active_habits_tree['columns'] = ("Habit Name", "Streak", "Interval", "Remaining Time", "Deadline")

            # Format Columns
            self.active_habits_tree.column("#0", width=0, minwidth=0)
            self.active_habits_tree.column("Habit Name", anchor="w", width=80, minwidth=25)
            self.active_habits_tree.column("Streak", anchor="center", width=50,minwidth=25)
            self.active_habits_tree.column("Interval", anchor="w", width=80,minwidth=25)
            self.active_habits_tree.column("Remaining Time", anchor="center", width=120, minwidth=25)
            self.active_habits_tree.column("Deadline", anchor="w", width=150, minwidth=50)
            
            # Create Headings
            self.active_habits_tree.heading("#0", text="", anchor="w") #Ghost column
            self.active_habits_tree.heading("Habit Name", text="Habit Name", anchor="w")
            self.active_habits_tree.heading("Streak", text="Streak", anchor="center")
            self.active_habits_tree.heading("Interval", text="Interval", anchor="w")
            self.active_habits_tree.heading("Remaining Time", text="Remaining Time", anchor="center")
            self.active_habits_tree.heading("Deadline", text="Deadline", anchor="w")

            # Get active user habits from the database using user_ID
            active_habits = self.db.get_active_habits(self.user_ID)
            # set a counter
            counter = 0
            for record in active_habits:
                # Calculate deadline
                self.last_check = record[4]  # Get last checkoff from database
                self.monitoring_interval = record[6]  # Get monitoring interval from database
                
                # Get the active habits ID from database and store it in variable for db.update.data function if failed
                self.data = {'status': 'failed'}
                self.active_habit_ID = record[0] 
                
                # Check if the stored monitoring interval is daily, weekly or monthly and calculate the remaining time for checkoff depending on the interval
                if self.monitoring_interval == "daily":
                    self.time_interval = timedelta(days=2)
                    # Calculate Deadline until user has to check off habit
                    # Get update_expiry from database
                    self.update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID",self.active_habit_ID)
                    self.deadline = self.update_expiry[0][0] # Extracts the datetime object from list
                    # Calculate Countdown
                    self.remaining_time = self.deadline - dt.now()
                    self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                    remaining_datetime = dt(1, 1, 1) + self.remaining_timedelta
                    # Format Countdown
                    remaining_days = self.remaining_time.days
                    remaining_time = remaining_datetime.time()
                    formatted_remaining_time = f"{remaining_days}d {remaining_time}"
                    if self.remaining_time.total_seconds() > 0:        
                        self.active_habits_tree.insert(parent="", index="end", iid=counter, text="", values=(record[1], record[5], record[6], str(formatted_remaining_time), self.deadline))
                        counter += 1
                    # if user fails to check off habit within timeframe the streak goes to zero
                    else:
                        formatted_remaining_time = "Time is up!"
                        self.active_habits_tree.insert(parent="", index="end", iid=counter,text ="", values=(record[1], record[5], record[6], formatted_remaining_time,self.deadline))
                        # Set status in active_habits_table to "failed"
                        self.db.update_data("active_user_habits", self.data,"active_habits", self.active_habit_ID)
                        counter += 1
                elif self.monitoring_interval == "weekly":
                    self.time_interval = timedelta(days=7)
                    # Calculate Deadline until user has to check off habit
                    self.update_expiry = self.db.check_value("update_expiry", "active_user_habits","active_habits_ID", self.active_habit_ID)
                    self.deadline = self.update_expiry[0][0]  # Extracts the datetime object from list
                    # Calculate Countdown
                    self.remaining_time = self.deadline - dt.now()
                    self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                    remaining_days = self.remaining_time.days
                    remaining_hours = self.remaining_timedelta.seconds // 3600
                    remaining_minutes = (self.remaining_timedelta.seconds % 3600) // 60
                    remaining_seconds = self.remaining_timedelta.seconds % 60
                    # Format Countdown
                    formatted_remaining_time = f"{remaining_days}d {remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"
                    if self.remaining_time.total_seconds() > 0:    
                        self.active_habits_tree.insert(parent="", index="end", iid=counter,text ="", values=(record[1], record[5], record[6], formatted_remaining_time, self.deadline))
                        counter += 1
                    else:
                        formatted_remaining_time = "Time is up!"
                        self.active_habits_tree.insert(parent="",index="end", iid=counter,text ="", values=(record[1], record[5], record[6], formatted_remaining_time, self.deadline))
                        # Set status in active_habits_table to "failed"
                        self.db.update_data("active_user_habits", self.data,"active_habits", self.active_habit_ID)
                        counter +=1
                # If the monitoring isn't daily or weekly it has to be monthly
                else:
                    self.time_interval = timedelta(days = 30)
                    # Calculate Deadline until user has to check off habit
                    self.update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID", self.active_habit_ID)
                    self.deadline = self.update_expiry[0][0]  # Extracts the datetime object from list
                    # Calculate Countdown
                    self.remaining_time = self.deadline - dt.now()
                    self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                    remaining_days = self.remaining_time.days
                    remaining_hours = self.remaining_timedelta.seconds // 3600
                    remaining_minutes = (self.remaining_timedelta.seconds % 3600) // 60
                    remaining_seconds = self.remaining_timedelta.seconds % 60
                    # Format Countdown
                    formatted_remaining_time = f"{remaining_days}d {remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"
                    if self.remaining_time.total_seconds() > 0:      
                        self.active_habits_tree.insert(parent="", index="end", iid=counter,text ="", values=(record[1], record[5], record[6], formatted_remaining_time, self.deadline))
                        counter += 1
                    else:
                        formatted_remaining_time = "Time is up!"
                        self.active_habits_tree.insert(parent="", index="end", iid=counter,text ="", values=(record[1], record[5], record[6], formatted_remaining_time, self.deadline))
                        # Set status in active_habits_table to "failed"
                        self.db.update_data("active_user_habits", self.data,"active_habits", self.active_habit_ID)
                        counter +=1

            # Schedule another call to the update_active_habits_tree function after every second
            self.after(1000, self.update_active_habits_tree)

    def update_active_habits_tree(self):
        """Updates the active user habits treeview, displaying the time remaining until the next checkoff deadline
        and updating the status of any habits that have not been checked off within the deadline.

        The function retrieves the active habits for the current user from the database and calculates the remaining time until
        the next checkoff deadline for each habit, based on the monitoring interval specified for that habit (daily, weekly, or monthly).
        If the remaining time is positive, the function updates the corresponding row in the treeview to display the time remaining in
        days, hours, minutes, and seconds. If the remaining time is negative, the function updates the corresponding row in the treeview
        to display "Time is up!" and updates the status of the habit to "failed" in the active_habits_table in the database.

        The function is called repeatedly using the tkinter after method, causing the treeview to be updated every x seconds.

        Args:
            self: The tkinter object.

        Returns:
            None.
        """

        # Get active user habits from the database using user_ID
        active_habits = self.db.get_active_habits(self.user_ID)
        # set a counter
        counter = 0
        for record in active_habits:
            # Calculate deadline
            self.last_check = record[3]  # Get last checkoff from database
            self.monitoring_interval = record[6] # Get monitoring interval from database

            # Get the active habits ID from database and store it in variable for db.update.data function if failed
            self.data = {'status': 'failed'}
            self.active_habit_ID = record[0] 
                        
            # Check if the stored monitoring interval is daily, weekly or monthly and calculate the remaining time for checkoff depending on the interval
            if self.monitoring_interval == "daily":
                self.time_interval = timedelta(days = 2)
                # Calculate Deadline until user has to check off habit
                self.update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID",self.active_habit_ID)
                self.deadline = self.update_expiry[0][0] # Extracts the datetime object from list
                # Calculate Countdown
                self.remaining_time = self.deadline - dt.now()
                self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                remaining_datetime = dt(1, 1, 1) + self.remaining_timedelta
                # Format Countdown
                remaining_days = self.remaining_time.days
                remaining_time = remaining_datetime.time()
                formatted_remaining_time = f"{remaining_days}d {remaining_time}"
                if self.remaining_time.total_seconds() > 0:        
                    self.active_habits_tree.set(counter,column = 3, value = formatted_remaining_time)
                    counter += 1
                # if user fails to check off habit within timeframe the streak goes to zero
                else:
                    formatted_remaining_time = "Time is up!"
                    #self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    self.active_habits_tree.set(counter,column = 3, value = formatted_remaining_time)
                    # Set status in active_habits_table to "failed"
                    self.db.update_data("active_user_habits",self.data,"active_habits",self.active_habit_ID)
                    counter += 1
            elif self.monitoring_interval == "weekly":
                self.time_interval = timedelta(days = 7)
                # Calculate Deadline until user has to check off habit
                self.update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID",self.active_habit_ID)
                self.deadline = self.update_expiry[0][0] # Extracts the datetime object from list
                # Calculate Countdown
                self.remaining_time = self.deadline - dt.now()
                self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                remaining_days = self.remaining_time.days
                remaining_hours = self.remaining_timedelta.seconds // 3600
                remaining_minutes = (self.remaining_timedelta.seconds % 3600) // 60
                remaining_seconds = self.remaining_timedelta.seconds % 60
                # Format Countdown
                formatted_remaining_time = f"{remaining_days}d {remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"
                if self.remaining_time.total_seconds() > 0:    
                    #self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    self.active_habits_tree.set(counter,column = 3, value = formatted_remaining_time)
                    counter += 1
                else:
                    formatted_remaining_time = "Time is up!"
                    #self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    self.active_habits_tree.set(counter,column = 3, value = formatted_remaining_time)
                    # Set status in active_habits_table to "failed"
                    self.db.update_data("active_user_habits",self.data,"active_habits",self.active_habit_ID)
                    counter +=1
            # If the monitoring isn't daily or weekly it has to be monthly
            else:
                self.time_interval = timedelta(days = 30)
                # Calculate Deadline until user has to check off habit
                self.update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID",self.active_habit_ID)
                self.deadline = self.update_expiry[0][0] # Extracts the datetime object from list
                # Calculate Countdown
                self.remaining_time = self.deadline - dt.now()
                self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                remaining_days = self.remaining_time.days
                remaining_hours = self.remaining_timedelta.seconds // 3600
                remaining_minutes = (self.remaining_timedelta.seconds % 3600) // 60
                remaining_seconds = self.remaining_timedelta.seconds % 60
                # Format Countdown
                formatted_remaining_time = f"{remaining_days}d {remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"
                if self.remaining_time.total_seconds() > 0:      
                    #self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    self.active_habits_tree.set(counter,column = 3, value = formatted_remaining_time)
                    counter += 1
                else:
                    formatted_remaining_time = "Time is up!"
                    #self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    self.active_habits_tree.set(counter,column = 3, value = formatted_remaining_time)
                    # Set status in active_habits_table to "failed"
                    self.db.update_data("active_user_habits",self.data,"active_habits",self.active_habit_ID)
                    counter +=1

        # Schedule another call to this function after every second
        self.after(1000, self.update_active_habits_tree)

    def delete_active_habit(self):
        """
        Deletes the selected active habit from the database by updating its status to 'deleted'.
        This function does not delete the active habit entirely from the database, but instead marks it as deleted,
        so that it will not be displayed in the active habits tree anymore.

        Returns:
        None.
        """
        # Get selected items
        selected_items = self.active_habits_tree.selection()

        # Loop through selected items and delete from database
        for item in selected_items:
            active_habit_name = self.active_habits_tree.item(item)["values"][0]
            print(active_habit_name)
            user_ID = self.user_ID
            print(user_ID)
            query = f"""UPDATE active_user_habits INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                        SET status = 'deleted'
                        WHERE active_user_habits.user_ID = {user_ID} AND habits.habit_name = '{active_habit_name}';                       
                        """
            # Use execute query function to execute the query and set the status to 'deleted' in the database for this active habit. 
            print(query)
            try:
                self.db.execute_query(query)
                messagebox.showinfo("Success","Habit not active any longer. Please update table.")
            except Error as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")


    def update_active_habits_table(self):
        """Updates the active habits treeview with the current user's active habits.

        Clears the treeview, retrieves the user's active habits from the database,
        and calculates the deadline for each habit based on its monitoring interval.
        If the user has not checked off the habit within the monitoring interval, the
        habit's status is set to 'failed' in the database and its streak is reset to 0.
        The active habits treeview displays the habit name, monitoring interval, remaining
        time until the next checkoff deadline, and the deadline itself.

        Args:
            self (object): The class instance.

        Returns:
            None
        """

        # Clear the treeview
        self.active_habits_tree.delete(*self.active_habits_tree.get_children())

        # Get active user habits from the database using user_ID
        active_habits = self.db.get_active_habits(self.user_ID)
        # set a counter
        counter = 0
        for record in active_habits:
            # Calculate deadline
            self.last_check = record[3]  # Get last checkoff from database
            self.monitoring_interval = record[6] # Get monitoring interval from database

            # Get the active habits ID from database and store it in variable for db.update.data function if failed
            self.data = {'status': 'failed'}
            self.active_habit_ID = record[0] 

            # Check if the stored monitoring interval is daily, weekly or monthly and calculate the remaining time for checkoff depending on the interval
            if self.monitoring_interval == "daily":
                self.time_interval = timedelta(days = 2)
                # Calculate Deadline until user has to check off habit
                self.update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID",self.active_habit_ID)
                self.deadline = self.update_expiry[0][0] # Extracts the datetime object from list
                # Calculate Countdown
                self.remaining_time = self.deadline - dt.now()
                self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                remaining_datetime = dt(1, 1, 1) + self.remaining_timedelta
                # Format Countdown
                remaining_days = self.remaining_time.days
                remaining_time = remaining_datetime.time()
                formatted_remaining_time = f"{remaining_days}d {remaining_time}"
                if self.remaining_time.total_seconds() > 0:        
                    self.active_habits_tree.insert(parent="", index="end", iid=counter, text="", values=(record[1], record[5], record[6], str(formatted_remaining_time), self.deadline))
                    counter += 1
                # if user fails to check off habit within timeframe the streak goes to zero
                else:
                    formatted_remaining_time = "Time is up!"
                    self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    # Set status in active_habits_table to "failed"
                    self.db.update_data("active_user_habits",self.data,"active_habits",self.active_habit_ID)                    
                    counter += 1
            elif self.monitoring_interval == "weekly":
                self.time_interval = timedelta(days = 7)
                # Calculate Deadline until user has to check off habit
                self.update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID",self.active_habit_ID)
                self.deadline = self.update_expiry[0][0]  # Extracts the datetime object from list
                # Calculate Countdown
                self.remaining_time = self.deadline - dt.now()
                self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                remaining_days = self.remaining_time.days
                remaining_hours = self.remaining_timedelta.seconds // 3600
                remaining_minutes = (self.remaining_timedelta.seconds % 3600) // 60
                remaining_seconds = self.remaining_timedelta.seconds % 60
                # Format Countdown
                formatted_remaining_time = f"{remaining_days}d {remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"
                if self.remaining_time.total_seconds() > 0:    
                    self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    counter += 1
                else:
                    formatted_remaining_time = "Time is up!"
                    self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    # Set status in active_habits_table to "failed"
                    self.db.update_data("active_user_habits",self.data,"active_habits",self.active_habit_ID)
                    counter +=1
            # If the monitoring isn't daily or weekly it has to be monthly
            else:
                self.time_interval = timedelta(days = 30)
                # Calculate Deadline until user has to check off habit
                self.update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID",self.active_habit_ID)
                self.deadline = self.update_expiry[0][0] # Extracts the datetime object from list
                # Calculate Countdown
                self.remaining_time = self.deadline - dt.now()
                self.remaining_timedelta = timedelta(seconds=self.remaining_time.seconds)
                remaining_days = self.remaining_time.days
                remaining_hours = self.remaining_timedelta.seconds // 3600
                remaining_minutes = (self.remaining_timedelta.seconds % 3600) // 60
                remaining_seconds = self.remaining_timedelta.seconds % 60
                # Format Countdown
                formatted_remaining_time = f"{remaining_days}d {remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"
                if self.remaining_time.total_seconds() > 0:      
                    self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    counter += 1
                else:
                    formatted_remaining_time = "Time is up!"
                    self.active_habits_tree.insert(parent="",index="end",iid=counter,text ="", values=(record[1],record[5],record[6],formatted_remaining_time,self.deadline))
                    # Set status in active_habits_table to "failed"
                    self.db.update_data("active_user_habits",self.data,"active_habits",self.active_habit_ID)
                    counter +=1

        # Schedule another call to this function after every second
        self.after(1000, self.update_active_habits_tree)

    def reactivate_active_habit(self):
        """
        Reactivate a habit with a dead streak. In the database the active habit has to be set to 'deleted' and and 
        a new entry has to be made with streak = 0. So the user has this "lost streak" saved for later analysis.
        starting_date has to be now. Interval stays the same as before.
        
        Args:
        self (object): The object itself.
        
        Returns:
        None. 
        """

        # Get selected items
        selected_items = self.active_habits_tree.selection()

        # Loop through selected items and delete from database
        for item in selected_items:
            active_habit_name = self.active_habits_tree.item(item)["values"][0]
            user_ID = self.user_ID
            habit_ID =  self.db.get_habit_ID(user_ID, active_habit_name)

            # Get the monitoring interval of the habit
            interval_ID = self.active_habits_tree.item(item)["values"][2]
            # convert the interval_ID from a string to a integer:
            if interval_ID == "daily":
                interval_ID = 1
            elif interval_ID == "weekly":
                interval_ID = 2
            else:
                interval_ID = 3            
            # Get the current status of the selected habit from the treeview
            status = self.active_habits_tree.item(item)["values"][3]
            
            # If the user fails to track the habit the staus is set to 'Time is up!' In this case the user can reactivate the habit. 
            if status == 'Time is up!':
               
                # Update status for old active user habit from failed to deleted
                query = f"""UPDATE active_user_habits
                            INNER JOIN habits ON active_user_habits.habit_ID = habits.habit_ID
                            SET status = 'deleted'
                            WHERE active_user_habits.user_ID = {user_ID} AND habits.habit_name = '{active_habit_name}' AND active_user_habits.status = 'failed';                  
                    """
                # Execute query to delete old_active_habit
                self.db.execute_query(query)
                
                # Depending on interval_ID set the new_update_expiry
                if interval_ID == 1:
                    new_update_expiry = dt.now() + timedelta(hours = 24)
                elif interval_ID == 2: 
                    new_update_expiry = dt.now() + timedelta(hours = 168)
                else: 
                    new_update_expiry = dt.now() + timedelta(hours = 720)
                # Create a new active user habit with the same information as the last one using the ActiveUserHabit class
                new_active_user_habit = ActiveUserHabit(user_ID, habit_ID, interval_ID, update_expiry=new_update_expiry)
                #Store the new active_user_habit in the variable data as a dictionary for inserting it into the database using the db.insert_data function
                data = vars(new_active_user_habit)
                data['habit_ID'] = data['habit_ID'][0] # convert the tuple to a integer using the first stored value
                # Insert the new active_user_habit in the database
                self.db.insert_data("active_user_habits", data)
                messagebox.showinfo("Success", "The Habit is now reactivated for tracking")

            # If the the selected habit is already set active for the user a error message pops up
            elif status == 'in progress':
                messagebox.showerror('Error','This habit is already active. You can delete it or go on. Stay active!')
            
            # If the status is already deleted only a new active_user_habit gets stored in the database 
            elif status == 'deleted':
                # Create a new active user habit with the same information as the last one
                new_active_user_habit = ActiveUserHabit(user_ID, habit_ID, interval_ID)
                # Store the new active_user_habit in the variable data as a dictionary for inserting it into the database using the db.insert_data function
                data = vars(new_active_user_habit)
                #print(active_user_habit)
                self.db.insert_data("active_user_habits", data)
                messagebox.showinfo("Success", "The Habit is now reactivated for tracking")
            else:
                messagebox.showerror('Error', 'No valid habit was selected for reactivation')
            
            print("done")

    def check_habit(self):
        """
        This Function is used for the Check Habbit button on the main_screen. If a user checks/tracks a habit the following should happen:
        1. The streak is set streak +=1 and stored in db
        2. The last_check attribute is updated to now.
        3. The update_expiry attribute is updated depending on the time_interval
        """
        # Get selected items
        selected_items = self.active_habits_tree.selection()

        # Loop through selected items and delete from database
        for item in selected_items:
            # Store all needed values from the database to the corresponding variables
            active_habit_name = self.active_habits_tree.item(item)["values"][0] # Get habit name from selected habit in tree
            user_ID = self.user_ID  # Get user_ID from stored user_ID from the logged in user
            habit_ID = int(self.db.get_habit_ID(user_ID, active_habit_name)[0]) # Get habit_ID from the habits table
            active_habits_ID = self.db.get_active_habit_ID(user_ID,habit_ID,"in progress")
            # Get current streak from treeview
            streak = self.db.get_streak(active_habits_ID)
            # Get last_check from database
            last_check = self.db.check_value("last_check","active_user_habits","active_habits_ID",active_habits_ID)
            # Get update_expiry from database
            update_expiry = self.db.check_value("update_expiry","active_user_habits","active_habits_ID",active_habits_ID)
            original_update_expiry = update_expiry[0][0] # Extracts the datetime object from list
            # Get the monitoring interval of the habit
            interval_ID = self.active_habits_tree.item(item)["values"][2] # Get interval_ID from selected active_user_habit
            
            # Convert the interval_ID from a string to a integer:
            if interval_ID == "daily":
                interval_ID = 1
                # Calculate the new update_expiry
                new_update_expiry = original_update_expiry + timedelta(days = 1)
                # Calculate the time difference between the new_update expiry and the actual time 
                time_diff = new_update_expiry - dt.now() 
                # Calculate how much time is left until user can check this habit again
                next_check = original_update_expiry - dt.now()
                if streak == 0: # If streak is 0 the habit was activated same day.
                    new_streak = streak +1
                    data = {"streak": new_streak,
                                "last_check": dt.now(),
                                "update_expiry": new_update_expiry}
                    self.db.update_data("active_user_habits", data, "active_habits", active_habits_ID)
                    next_check = (new_update_expiry - timedelta(days=1)) - dt.now()
                    messagebox.showinfo("Success",f"Congrats! You have checked you daily habit and you streak continoues. Your next check is available in {next_check}. Stay focused!")
                elif next_check > timedelta(days = 1):
                    next_check = (original_update_expiry - timedelta(days=1)) - dt.now()
                    messagebox.showinfo("Info",f"This habit was already checked during this time period. You can check it again in {next_check}")
                else:
                    new_streak = streak +1
                    data = {"streak": new_streak,
                            "last_check": dt.now(),
                            "update_expiry": new_update_expiry}
                    next_check = (new_update_expiry - timedelta(days=1)) - dt.now()
                    self.db.update_data("active_user_habits", data, "active_habits", active_habits_ID)
                    messagebox.showinfo("Success",f"Congrats! You have checked you daily habit and you streak continoues. Your next check is available in {next_check}. Stay focused!")
            # Check if interval = weekly
            elif interval_ID == "weekly":
                interval_ID = 2
                # Calculate the new update_expiry
                new_update_expiry = original_update_expiry + timedelta(days = 7)
                # Calculate the time difference between the new_update expiry and the actual time 
                time_diff = new_update_expiry - dt.now() 
                # Calculate how much time is left until user can check this habit again
                next_check = original_update_expiry - dt.now()
                if streak == 0: # If streak is 0 the habit was activated same week.
                    new_streak = streak +1
                    data = {"streak": new_streak,
                                "last_check": dt.now(),
                                "update_expiry": new_update_expiry}
                    self.db.update_data("active_user_habits", data, "active_habits", active_habits_ID)
                    next_check = (new_update_expiry - timedelta(days=7)) - dt.now()
                    messagebox.showinfo("Success",f"Congrats! You have checked you daily habit and you streak continoues. Your next check is available in {next_check}. Stay focused!")
                elif next_check > timedelta(days = 7):
                    next_check = (original_update_expiry - timedelta(days=7)) - dt.now()
                    messagebox.showinfo("Info",f"This habit was already checked during this time period. You can check it again in {next_check}")
                else:
                    new_streak = streak +1
                    data = {"streak": new_streak,
                            "last_check": dt.now(),
                            "update_expiry": new_update_expiry}
                    next_check = (new_update_expiry - timedelta(days=7)) - dt.now()
                    self.db.update_data("active_user_habits", data, "active_habits", active_habits_ID)
                    messagebox.showinfo("Success",f"Congrats! You have checked you daily habit and you streak continoues. Your next check is available in {next_check}. Stay focused!")
            # Check if time interval = monthly
            elif interval_ID == "monthly":
                interval_ID = 3
                # Calculate the new update_expiry
                new_update_expiry = original_update_expiry + timedelta(days = 30)
                # Calculate the time difference between the new_update expiry and the actual time 
                time_diff = new_update_expiry - dt.now() 
                # Calculate how much time is left until user can check this habit again
                next_check = original_update_expiry - dt.now()
                if streak == 0: # If streak is 0 the habit was activated same month.
                    new_streak = streak +1
                    data = {"streak": new_streak,
                                "last_check": dt.now(),
                                "update_expiry": new_update_expiry}
                    self.db.update_data("active_user_habits", data, "active_habits", active_habits_ID)
                    next_check = (new_update_expiry - timedelta(days=30)) - dt.now()
                    messagebox.showinfo("Success",f"Congrats! You have checked you daily habit and you streak continoues. Your next check is available in {next_check}. Stay focused!")
                elif next_check > timedelta(days = 30):
                    next_check = (original_update_expiry - timedelta(days=30)) - dt.now()
                    messagebox.showinfo("Info",f"This habit was already checked during this time period. You can check it again in {next_check}")
                else:
                    new_streak = streak +1
                    data = {"streak": new_streak,
                            "last_check": dt.now(),
                            "update_expiry": new_update_expiry}
                    next_check = (new_update_expiry - timedelta(days=30)) - dt.now()
                    self.db.update_data("active_user_habits", data, "active_habits", active_habits_ID)
                    messagebox.showinfo("Success",f"Congrats! You have checked you daily habit and you streak continoues. Your next check is available in {next_check}. Stay focused!")
                # Else print a error message for wrong time interval
            else:
                messagebox.showerror("Error","There is something wrong with the Interval")

    def update_time(self):
        """Function to update the time label on the bottom of the screen.

        This function gets the current time and sets the text of the time label to it.
        It uses the after() method to call itself every second, effectively updating the label in real-time.
        """
        self.current_time = dt.now().strftime('%H:%M:%S')
        self.time_label.configure(text=self.current_time)
        self.time_label.after(1000, self.update_time)  # Update every second
    
    def close_application(self):
        """Function to close the Habit Tracker application.

        This function prompts the user with a confirmation message before closing the application.
        If the user confirms, the function destroys the main window and exits the application.
        """
        confirm_exit = messagebox.askyesno("Confirm Exit", "Do you really want to leave the Habit Tracker?")
        if confirm_exit:
            self.destroy() # Close the main window and exit the application
 
    def open_myHabits(self):
        """
        Creates a new popup window that displays a table of the user's habits. 
        Adds several buttons to interact with the habits, including adding a new habit, 
        deleting a habit, updating the habit table, and activating a selected habit.
        """
        # Create a new window
        popup = tk.Toplevel(self)
        popup.title("MyHabits")
        #popup.grab_set() # Disables interaction with parent window

        # get the all habits of the user
        habits = self.db.get_user_habits(self.user_ID)
        
        # Create a frame to hold the table and buttons
        frame = tk.Frame(popup)
        frame.pack(padx=20, pady=20)

        # Check if there are any habits to display
        if not habits:
        # Display a message to the user
            message_label = tk.Label(frame, text="No habits to display")
            message_label.pack()
        
        else:
            # Create a treeview widget to display the habits
            tree = ttk.Treeview(frame, columns=("no","habit_name", "description" ,"creation_date", "category","habit_ID"),show = "headings")
            #tree.heading("#0",text="ID")
            tree.heading("#1",text="No.")
            tree.heading("#2", text="Habit Name")
            tree.heading("#3", text="Description")
            tree.heading("#4", text="Creation Date")
            tree.heading("#5", text="Category")
            tree.heading("#6", text = "Habit ID")
            tree.pack(side="left")

            # Insert habits into the treeview and start counting by 1 for each habit of each user
            counter = 0
            for habit in habits:
                counter += 1
                item = tree.insert("","end",values = (counter, habit[1], habit[2], habit[3], habit[4], habit[0], ""))

        # Create a frame for the buttons
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        # Add a button for adding habits
        add_button = tk.Button(button_frame, text="Add Habit", command=lambda: self.add_habit())
        add_button.pack(side="left", padx=5)

        # Add a button for deleting habits
        delete_button = tk.Button(button_frame, text="Delete Habit", command=lambda: self.delete_habits(tree))
        delete_button.pack(side="left", padx=5)

        # Add a button for updating the habit table
        update_button = tk.Button(button_frame, text="Update Table", command=lambda: self.update_habits_table(tree))
        update_button.pack(side="left", padx=5)

        # Add a button for activating a selected habit from the table
        activate_button = tk.Button(button_frame, text="Activate Habit", command=lambda: self.activate_habit(tree))
        activate_button.pack(side="left", padx=5)

        # Wait for a popup window to be destroyed
        popup.wait_window()
    
    # When pushing the Update Table button the screen gets updated with the newest habits
    def update_habits_table(self, tree):
        """
        Update the habit table displayed in the MyHabits popup window with the latest data from the database.

        Args:
            tree (ttk.Treeview): The treeview widget displaying the habit table.

        Returns:
            None
        """
        # Refresh the habit table by getting the latest data from the database
        habits = self.db.get_user_habits(self.user_ID)
        
        # Clear the treeview and insert the updated data
        tree.delete(*tree.get_children())
        
        # Set a counter for giving each user Habit a individual number starting from 1
        counter = 0
        for habit in habits:
            counter += 1
            item = tree.insert("","end",values = (counter, habit[1], habit[2], habit[3], habit[4], habit[0], ""))
        
        # Reset the counter variable to 0
        counter = 0

    def delete_habits(self, tree):
        """Delete the selected habit and its corresponding records from the active_user_habits table.

        Args:
            tree (ttk.Treeview): The treeview widget that displays the habit table.

        Returns:
            None.
        """
        # Get selected items
        selected_items = tree.selection()

        # Loop through selected items and delete from database
        for item in selected_items:
            habit_ID = tree.item(item)["values"][5]
            sys_user_habits = self.db.get_user_habits(99)

            # Check if the habit ID is in the user's habits
            if habit_ID in [value[0] for value in sys_user_habits]:
                messagebox.showerror("Error", "Cannot delete a system habit!")
            else:
                confirmation = messagebox.askyesno("Confirm deletion", "Do you really want to delete this habit and its corresponding records from the active_user_habits table? Your streaks and history for this habit will be deleted.")
                if confirmation:
                    # Delete habit and its corresponding records from the database
                    self.db.delete_habit(habit_ID)
                    
                    # Refresh the habit table
                    self.update_habits_table(tree)
    

    # Open window for adding new habit by user if pushing the Add Habit Button
    def add_habit(self):
        """
        Opens a pop-up window for the user to add a new habit to their account.
        The window includes fields for entering the habit name, description, and category.
        If the user successfully saves the habit, the habit is added to the database and the habit table is refreshed.
        """
               
        self.popup = tk.Toplevel(self)
        self.popup.geometry("300x250")
        self.popup.title("Add Habits to MyHabits")
        self.popup.grab_set() # Disables interaction with parent window

        self.login_label = tk.Label(self.popup, text="Please enter habit below:")
        self.login_label.pack()
        tk.Label(self.popup, text="").pack()

        # Create Label and Entry for habit_name
        self.habit_name_label = tk.Label(self.popup, text="Habit Name")
        self.habit_name_label.pack()
        self.entry_habit_name = tk.Entry(self.popup)
        self.entry_habit_name.pack()

        # Create Label and Entry for description
        self.description_label = tk.Label(self.popup, text="Description")
        self.description_label.pack()
        self.entry_description = tk.Entry(self.popup)
        self.entry_description.pack()

        # Create Label and Dropdown menu for category
        self.category_label = tk.Label(self.popup, text="Category")
        self.category_label.pack()
        self.category_var = tk.StringVar()
        self.entry_category = ttk.Combobox(self.popup, textvariable=self.category_var, state="readonly")
        self.entry_category.pack()
        categories = self.db.get_user_categories_name(self.user_ID) # get list of available categories from database
        self.entry_category['values'] = categories


        tk.Button(self.popup, text="Save new myHabit", command = self.save_habit, width=20, height=1).pack()

        self.popup.wait_window()  # Wait for popup window to be destroyed

    # Function for storing the input user data in the database and closing the popup window
    def save_habit(self):
        """
        Saves the habit entered by the user in the add_habit window to the database.
        The function retrieves the habit name, description, and category from the entries in the window.
        If any of the fields are empty, an error message is displayed.
        If the user already has a habit with the same name stored in the database, an error message is displayed.
        If there is already a system habit with the same name in the database, an error message is displayed.
        If everything is correct, the habit is saved to the database and a success message is displayed.
        """

        habit_name = self.entry_habit_name.get()
        description = self.entry_description.get()
        category_name = self.category_var.get()
        user_ID = self.user_ID
        category_ID = self.db.get_category_ID(category_name, user_ID)
        system_user_ID = 99
           
        # Check if any of the variables are empty
        if not all([habit_name, description, category_ID]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Check if the user already has a habit with the same name stored in the database
        existing_habit = self.db.get_habit_ID(user_ID, habit_name)
        if existing_habit:
            messagebox.showerror("Error", "You already have a habit with the same name stored. Please choose a different name.")
            return
        
        # Check if there is already a system habit with this name in the database
        system_habit = self.db.get_habit_ID(system_user_ID, habit_name)
        if system_habit:
            messagebox.showerror("Error", "There is already a predefined habit with the same name in the database. Please choose a different name or use the existing habit.")
            return

        # Use User class to create a new user instance
        new_habit = Habit(habit_name, user_ID, category_ID, description)
        #data = {'habit_name': habit_name, 'user_ID': user_ID, 'category_ID': category_ID, 'description': description}
        data = new_habit.create_dict()

        try:
            # If everything is correct a new user is saved in the database
            self.db.insert_data("habits", data)
            messagebox.showinfo("Success", "Habit: {} successfully saved".format(habit_name))
            self.popup.destroy()

        except mysql.connector.IntegrityError as e:
            # Catch the exception thrown if the username already exists
            messagebox.showerror("Error", "An error occurred: {}".format(str(e)))
            print("MySQL error: {}".format(e))
            self.popup.destroy()

    def activate_habit(self, tree):
        """Creates a popup window to activate a habit selected in a treeview widget.
        User has to select the control interval and optional streak targets or
        an ending date.
        
        Args:
        tree: A tkinter ttk.Treeview widget containing the habits to activate.
        
        Returns:
        None
        """
        # Get selected item
        selected_items = tree.selection()

        # Loop through selected items and get information about the habit_ID
        for item in selected_items:
            habit_ID = tree.item(item)["values"][5]

        habit_name = self.db.check_value("habit_name", "habits", "habit_ID", habit_ID)

        # Create popup window
        popup_window = tk.Toplevel()
        popup_window.title(f"Activate Habit {habit_name}")
        popup_window.geometry('600x200')

        # Get user ID
        #username = os.getenv("User_Variables").split(',')[0]
        username = self.username
        user_ID = self.db.get_userID(username)
       
       # Create labels and entry widgets for control frequency, goal streak, and end date
        control_interval_label = tk.Label(popup_window, text='Please choose the control interval:')
        control_interval_label.grid(column=0, row=0, pady=10, padx=10)

        # Define options
        self.interval_options = {1: "daily", 2: "weekly", 3: "monthly"}

        control_interval_var = tk.StringVar(value= 'daily' ) # Default Value when opening the window
        control_interval_dropdown = tk.OptionMenu(popup_window, control_interval_var, 'daily', 'weekly', 'monthly')
        control_interval_dropdown.grid(column=1, row=0, pady=10, padx=10)

        goal_streak_label = tk.Label(popup_window, text='Do you have a goal for a streak? If not leave it empty')
        goal_streak_label.grid(column=0, row=1, pady=10, padx=10)
        goal_streak_entry = tk.Entry(popup_window)
        goal_streak_entry.grid(column=1, row=1, pady=10, padx=10)

        end_date_label = tk.Label(popup_window, text='Do you want to set a fixed end date? If not leave it empty.')
        end_date_label.grid(column=0, row=2, pady=10, padx=10)

        # Create a DateEntry widget for selecting the end date
        end_date_var = tk.StringVar()
        end_date_entry = tkcalendar.DateEntry(popup_window, width=12, textvariable=end_date_var, date_pattern='YYYY-MM-DD')
        end_date_entry.delete(0, "end") # Clears the calendar widget when open the window. So its empty as default
        end_date_entry.grid(column=1, row=2, pady=10, padx=10)


        # Create save button
        def save_activation(self):
            """
            Activates a user's habit for tracking and saves it to the database.

            Reads the user's input for the habit activation form (control interval,
            goal streak, and end date) and converts it to the appropriate data types.
            Checks if the chosen end date is not in the past, and if the habit is not
            already active for the user. If the checks pass, creates a new instance of
            ActiveUserHabit with the provided data, calculates the update expiry time
            based on the control interval, and inserts the new habit into the
            active_user_habits table in the database using the db.insert_data function.

            Returns:
                None.
            """
            # Use the dictionary to get the corresponding Interval_ID for the database table monitoring_interval
            self.interval_options = {"daily" : 1,"weekly" : 2,"monthly": 3}
            self.interval_ID = self.interval_options[control_interval_var.get()]
            
            # Get entry for the goal streak
            self.goal_streak = goal_streak_entry.get()
            
            # Convert the end_date string to a datetime object
            self.end_date = end_date_var.get()
            if self.end_date:
                self.end_date = dt.strptime(self.end_date, '%Y-%m-%d').date()

            # Set Last_check to now when activating a habit
            self.last_check = dt.now()
            
            # Check if chosen end date isn't in the past. Also possible that there is no end date, then store self.end_date as none
            if not self.end_date or self.end_date > dt.now().date():
                # check if the habit already set active for the user
                habit_exists = self.db.execute_query(f"SELECT * FROM active_user_habits WHERE user_ID = {user_ID} AND habit_ID = {habit_ID} AND status != 'deleted'")
                if habit_exists:
                    messagebox.showerror("Error", "This habit is already active for tracking!")
                    popup_window.destroy()
                else:
                    if self.interval_ID == 1:
                        # Set the time interval to 24 hours to add it to the last_check as update expiry
                        self.time_add_interval = timedelta(days = 1)
                        self.update_expiry = self.last_check + self.time_add_interval
                        # Create new instance of ActiveUserHabit
                        active_user_habit = ActiveUserHabit(user_ID, habit_ID, self.interval_ID, self.goal_streak, self.end_date, self.last_check, self.update_expiry)
                        # Store the new active_user_habit in the variable data as a dictionary for inserting it into the database using the db.insert_data function
                        data = vars(active_user_habit)
                        #print(active_user_habit)
                        self.db.insert_data("active_user_habits", data)
                        messagebox.showinfo("Success", "The Habit is now set active for tracking")
                        popup_window.destroy()
                    elif self.interval_ID == 2:
                        # Set the time interval to 7 days to add it to the last_check as update expiry
                        self.time_add_interval = timedelta(days = 7)
                        self.update_expiry = self.last_check + self.time_add_interval
                        # Create new instance of ActiveUserHabit
                        active_user_habit = ActiveUserHabit(user_ID, habit_ID, self.interval_ID, self.goal_streak, self.end_date, self.last_check, self.update_expiry)
                        # Store the new active_user_habit in the variable data as a dictionary for inserting it into the database using the db.insert_data function
                        data = vars(active_user_habit)
                        #print(active_user_habit)
                        self.db.insert_data("active_user_habits", data)
                        messagebox.showinfo("Success", "The Habit is now set active for tracking")
                        popup_window.destroy()
                    elif self.interval_ID == 3:
                        # Set the time interval to 30 days to add it to the last_check
                        self.time_add_interval = timedelta(days = 30)
                        self.update_expiry = self.last_check + self.time_add_interval
                        # Create new instance of ActiveUserHabit
                        active_user_habit = ActiveUserHabit(user_ID, habit_ID, self.interval_ID, self.goal_streak, self.end_date, self.last_check, self.update_expiry)
                        # Store the new active_user_habit in the variable data as a dictionary for inserting it into the database using the db.insert_data function
                        data = vars(active_user_habit)
                        #print(active_user_habit)
                        self.db.insert_data("active_user_habits", data)
                        messagebox.showinfo("Success", "The Habit is now set active for tracking")
                        popup_window.destroy()
            else:
                messagebox.showerror("Error", "Your end date is in the past! Please try again")
                popup_window.destroy()

        save_button = tk.Button(popup_window, text='Save', command=lambda: save_activation(self))
        save_button.grid(column=0, row=3, pady=10, padx=10, columnspan=2)
        
    def open_myCategories(self):
        """
        Opens a new window displaying all the categories of the current user, along with options to add, delete, and update categories.

        Returns:
        None
        """
        # Create a new window
        cat_popup = tk.Toplevel(self)
        cat_popup.title("MyCategories")
        cat_popup.grab_set() # Disables interaction with parent window

        # get the all categories of the user
        categories = self.db.get_user_categories(self.user_ID)
        
        # Create a frame to hold the table and buttons
        frame = tk.Frame(cat_popup)
        frame.pack(padx=20, pady=20)

        # Check if there are any habits to display
        if not categories:
        # Display a message to the user
            message_label = tk.Label(frame, text="No categories to display")
            message_label.pack()
        
        else:
            # Create a treeview widget to display the categories
            tree = ttk.Treeview(frame, columns=("no","category_name", "description" ,"creation_date", "category_ID"),show = "headings")
            #tree.heading("#0",text="ID")
            tree.heading("#1",text="No.")
            tree.heading("#2", text="Category Name")
            tree.heading("#3", text="Description")
            tree.heading("#4", text="Creation Date")
            tree.heading("#5", text = "Category ID")
            tree.pack(side="left")

            # Insert habits into the treeview and start counting by 1 for each category of each user
            counter = 0
            for category in categories:
                counter += 1
                item = tree.insert("","end",values = (counter, category[1], category[2], category[3], category[0], ""))

        # Create a frame for the buttons
        button_frame = tk.Frame(cat_popup)
        button_frame.pack(pady=10)

        # Add a button for adding categories
        add_button = tk.Button(button_frame, text="Add Category", command = self.add_category)
        add_button.pack(side="left", padx=5)

        # Add a button for deleting categories
        delete_button = tk.Button(button_frame, text="Delete Category", command = lambda: self.delete_category(tree))
        delete_button.pack(side="left", padx=5)

        # Add a button for updating the category table
        update_button = tk.Button(button_frame, text="Update Table", command = lambda: self.update_categories_table(tree))
        update_button.pack(side="left", padx=5)

    def update_categories_table(self, tree):
        """
        Updates the category table with the latest data from the database.

        Args:
            tree (ttk.Treeview): The treeview widget displaying the categories.
        """
        # Refresh the category table by getting the latest data from the database
        categories = self.db.get_user_categories(self.user_ID)
        
        # Clear the treeview and insert the updated data
        tree.delete(*tree.get_children())
        
        # Set a counter for giving each user category a individual number starting from 1
        counter = 0
        for category in categories:
            counter += 1
            item = tree.insert("","end",values = (counter, category[1], category[2], category[3], category[0], ""))
        
        # Reset the counter variable to 0
        counter = 0
    
    # Function for the delete button
    def delete_category(self, tree):
        """
        Deletes the selected category from the database and updates the category table using delete_category function
        from MySQLDatabase class.

        Args:
            tree (ttk.Treeview): The treeview widget displaying the categories.
        """
        # Get selected items
        selected_items = tree.selection()

        # Loop through selected items and delete from database
        for item in selected_items:
            category_ID = tree.item(item)["values"][4]
            sys_user_categories = self.db.get_user_categories(99)
            
            #Check if category is one of the sys users categories
            if category_ID in [value[0] for value in sys_user_categories]:
                messagebox.showerror("Error", "Can't delete a predefined sys user category")
            else:
                confirmation = messagebox.askyesno("Confirm deletion", "Do you really want to delete this category?")
                if confirmation:
                    # Use delete_category function from database class to delete selected category from the database
                    self.db.delete_category(category_ID)
                    # Refresh the habit table
                    self.update_categories_table(tree)

    def add_category(self):
        """
        Open a popup window for the user to add a new category to their list.
        Uses save_category function to store new category in database when clicking
        the respective button.        
        """

        self.add_cat_pop = tk.Toplevel()
        self.add_cat_pop.geometry("300x250")
        self.add_cat_pop.title("Add Categories to MyCategories")
        self.add_cat_pop.grab_set() # Disables interaction with parent window

        self.login_label = tk.Label(self.add_cat_pop, text="Please enter category below:")
        self.login_label.pack()
        tk.Label(self.add_cat_pop, text="").pack()

        # Create Label and Entry for category_name
        self.category_name_label = tk.Label(self.add_cat_pop, text="Category Name")
        self.category_name_label.pack()
        self.entry_category_name = tk.Entry(self.add_cat_pop)
        self.entry_category_name.pack()

        # Create Label and Entry for description
        self.description_label = tk.Label(self.add_cat_pop, text="Description")
        self.description_label.pack()
        self.entry_description = tk.Entry(self.add_cat_pop)
        self.entry_description.pack()

        tk.Button(self.add_cat_pop, text="Save new myCategory", command = self.save_category, width=20, height=1).pack()

        self.add_cat_pop.wait_window() # Wait for popup window to be destroyed


    def save_category(self):     
        """
        Save the new category entered by the user to the database using insert_data function
        from MySQLDatabase class and destroyes popup window after finishing successfully.
        """
        category_name = self.entry_category_name.get()
        description = self.entry_description.get()
        user_ID = self.user_ID
            
        # Check if any of the variables are empty
        if not all([category_name, description]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Use Category class to create a new category instance
        new_category = Category(category_name, user_ID, description)
        data = new_category.create_dict()
                    
        try:
            # If everything is correct a new user is saved in the database
            self.db.insert_data("category", data)
            messagebox.showinfo("Success", "Category: {} successfully saved".format(category_name))
            self.add_cat_pop.destroy()
        except mysql.connector.IntegrityError as e:
            # Catch the exception thrown if the username already exists
            messagebox.showerror("Error", "An error occurred: {}".format(str(e)))
            print("MySQL error: {}".format(e))
            self.add_cat_pop.destroy()
     
    def update_profile(self):
        """
        Function for opening a window where a user can change their user credentials.
        Displays the current user credentials and allows the user to input new ones.
        Upon clicking 'Save Changes', the updated user credentials are stored in the database.

        Returns:
            None.
        """
        self.profile_popup = tk.Toplevel(self)
        self.profile_popup.title = ("Update your user credentials")
        self.profile_popup.geometry("400x400")
        self.profile_popup.grab_set() # Disables interaction with parent window


        #self.username = "SYS"
        active_user_ID = self.db.get_userID(self.username)
        # active_user_ID = int(os.getenv("active_user_ID"))
        
        user_dict = self.db.get_user_credentials(active_user_ID)
        
        # pady for adding spacing between widgets
        pady = 5

        # Create Label and Entry for first_name
        self.new_first_name_label = tk.Label(self.profile_popup, text=f"Saved First Name = {user_dict['first_name']}", pady = pady)
        self.new_first_name_label.pack()
        self.entry_new_first_name = tk.Entry(self.profile_popup)
        self.entry_new_first_name.pack()

        # Create Label and Entry for last_name
        self.new_last_name_label = tk.Label(self.profile_popup, text=f"Saved Last Name = {user_dict['last_name']}", pady=pady)
        self.new_last_name_label.pack()
        self.entry_new_last_name = tk.Entry(self.profile_popup)
        self.entry_new_last_name.pack()

        # Create Label and Entry for username
        self.new_username_label = tk.Label(self.profile_popup, text=f"Saved Username= {user_dict['username']}", pady=pady)
        self.new_username_label.pack()
        self.entry_new_username = tk.Entry(self.profile_popup)
        self.entry_new_username.pack()

        # Create Label and Entry for password
        self.new_password_label = tk.Label(self.profile_popup, text=f"Password = {user_dict['password']}", pady=pady)
        self.new_password_label.pack()
        self.entry_new_password = tk.Entry(self.profile_popup)
        self.entry_new_password.pack()

        # Create Label and Entry for email
        self.new_email_label = tk.Label(self.profile_popup, text=f"Email = {user_dict['email']}", pady=pady)
        self.new_email_label.pack()
        self.entry_new_email = tk.Entry(self.profile_popup)
        self.entry_new_email.pack()

        # Create Label and Entry for Phone_number
        self.new_phone_number_label = tk.Label(self.profile_popup, text=f"Phone_number = {user_dict['phone_number']}", pady=pady)
        self.new_phone_number_label.pack()
        self.entry_new_phone_number = tk.Entry(self.profile_popup)
        self.entry_new_phone_number.pack()

        tk.Button(self.profile_popup, text="Save changes", command = self.save_profile_changes, width=10, height=1).pack()

        self.profile_popup.wait_window()  # Wait for popup window to be destroyed

    def save_profile_changes(self):
        """
        Save changes for the user credentials in the database.

        Retrieves the new user entries from the entry widgets and updates the corresponding values in the user's database
        record. If the user inputs a new phone number or email address, the method checks that the phone number contains only
        digits and the email address contains an '@' symbol.

        Raises:
            Error: If the phone number entered contains non-numeric characters or the email address entered does not contain
            an '@' symbol.

        Returns:
            None.
        """
        
        # Get all new entries of the user
        new_first_name = self.entry_new_first_name.get()
        new_last_name = self.entry_new_last_name.get()
        new_username = self.entry_new_username.get()
        new_password = self.entry_new_password.get()
        new_email = self.entry_new_email.get()
        new_phone_number = self.entry_new_phone_number.get()

        # Get the user_ID value of the active habit tracker user from the environmental variable
        active_user_ID = int(os.getenv("active_user_ID"))
        
        # Get all stored credentials of the user stored in the database
        user_dict = self.db.get_user_credentials(active_user_ID)

        # Check if the phone number entered contains only numbers
        if new_phone_number and not new_phone_number.isnumeric():
            messagebox.showerror("Error", "Phone number must contain only digits")
            return

        # Check if the email address entered contains an '@' symbol
        if new_email and '@' not in new_email:
            messagebox.showerror("Error", "Invalid email address")
            return

        # Update the used dictionary (user_dict) for the user credentials with the new values if the user inputs some
        if new_first_name:
            user_dict['first_name'] = new_first_name
        if new_last_name:
            user_dict['last_name'] = new_last_name
        if new_username:
            user_dict['username'] = new_username
        if new_password:
            user_dict['password'] = new_password
        if new_email:
            user_dict['email'] = new_email
        if new_phone_number:
            user_dict['phone_number'] = new_phone_number
        
        # Set the value for last profile update to now and update the user_dict
        self.last_update = dt.now()
        user_dict['last_update'] = self.last_update
        
        # Use function from database class for updating the values in the database
        self.db.update_data("user_table",user_dict, "user", active_user_ID)
        
        # Print out message box 
        messagebox.showinfo("Success", "Profile changes successfully saved")
        
        # Close Profile Update Window
        self.profile_popup.destroy()
    
    def open_analyze_myhabits(self):
        """Opens a new window for analyzing the user's habits.

        This method creates a new window where the user can choose one of several predefined analyses to carry out.
        The user's selection is stored in the 'selected_option' attribute. The method also creates a button to update the table showing the results of the analysis.
        """
        # Create a new window
        self.analyse_popup = tk.Toplevel(self)
        self.analyse_popup.title("Analyse MyHabits")
        self.analyse_popup.geometry("600x600")
        self.analyse_popup.grab_set() # Disables interaction with parent window

        # Create a Label with a question
        Label_1 = tk.Label(self.analyse_popup, text='Which analysis do they want to carry out? Please choose one: ')
        Label_1.pack()
        
        # Define the different possible analysis
        self.option_1 = "Longest active streaks" # Shows a user the longest streaks
        self.option_2 = "Same Habit started" # Shows how often a user started tracking a habit
        self.option_3 = "completion of Streak Targets in %" # Shows the user the active habits with a Goal_Streak and how long to go until completion
        self.option_4 = "completion of Streak Targets in streak/target" # Shows the user the active habits with a Goal_Streak and how long to go until completion
        dropdown_options = {1: self.option_1, 2: self.option_2, 3: self.option_3, 4: self.option_4}

        # Create a StringVar to store the selected option
        self.selected_option = tk.StringVar(self.analyse_popup, self.option_1)

        # Create Dropdown menu for choosing predefined analysis
        analysis_dropdown = tk.OptionMenu(self.analyse_popup, self.selected_option, self.option_1, self.option_2, self.option_3, self.option_4)
        analysis_dropdown.pack()

        # Button to update the table
        update_button = tk.Button(self.analyse_popup, text="Update Table", command=self.update_analyse_table)
        update_button.pack()

    # Function to Update the table depending on the users choice
    def update_analyse_table(self):
        """
        Update the analysis table based on the user's choice.

        This function retrieves data from the database and displays it in a table or chart depending on the user's choice.
        The function destroys any existing treeview widget to prevent overlapping.

        The user has 4 different options to choose from.
        """
        # First check if treeview widgets exits and if so destroy it. This prevents overlapping.
        for child in self.analyse_popup.winfo_children():
            if isinstance(child, ttk.Treeview):
                child.destroy()

        # Get selected user option
        analysis = self.selected_option.get()
        user_ID = self.user_ID
        # Depending on users choice a specific table opens
        if analysis == self.option_1:
            # Get all active habits and sort them by the streak decreasing
            active_user_habits = self.db.get_all_active_habits(user_ID)
            
            if not active_user_habits:
                # Display a message to the user if no active habits/streaks to display
                message_label = tk.Label(frame, text="No habits/streaks to display")
                message_label.pack()
            else:
                # Create a Treeview Widget for the longest active streaks
                self.option_1_tree = ttk.Treeview(self.analyse_popup)
                self.option_1_tree.place(x = 50, y = 150)
                
                frame = tk.Frame(self.analyse_popup)
                frame.pack(padx=20, pady=20)
                
                # Define Columns
                self.option_1_tree['columns'] = ("Rank","Habit Name","Streak", "Interval","Status","Starting Date")

                # Format Columns
                self.option_1_tree.column("#0", width=0, minwidth=0) # Remove Ghost column
                self.option_1_tree.column("Rank", width=70, minwidth=25)
                self.option_1_tree.column("Habit Name", anchor="w", width=100, minwidth=60)
                self.option_1_tree.column("Streak", anchor="center", width=50,minwidth=50)
                self.option_1_tree.column("Interval", anchor="w", width=60,minwidth=60)
                self.option_1_tree.column("Status", anchor="center", width=100,minwidth=25)
                self.option_1_tree.column("Starting Date", anchor="w", width=150,minwidth=50)
                
                # Create Headings
                self.option_1_tree.heading("#0",text="", anchor="w") # Remove Ghost column
                self.option_1_tree.heading("Rank",text="Rank no. ", anchor="w")
                self.option_1_tree.heading("Habit Name",text="Habit Name", anchor="w")
                self.option_1_tree.heading("Streak",text="Streak", anchor="center")
                self.option_1_tree.heading("Interval",text="Interval", anchor="w")
                self.option_1_tree.heading("Status",text="Status", anchor="center")
                self.option_1_tree.heading("Starting Date",text="Starting Date", anchor="w")
                
                # Set a counter for inserting records
                counter = 0

                for record in active_user_habits:
                    counter +=1
                    item = self.option_1_tree.insert(parent="",index="end",iid = counter,text = "", values = (counter,record[1], record[5], record[6], record[7],record[2]))

        elif analysis == self.option_2:
            ''' This option returns a bar chart which sums up how a often a user already started the same habit again
            '''
            # Get all records from the active habits table
            active_user_habits = self.db.get_all_active_habits(user_ID)
                
            # Create a pandas dataframe for calculation of the failrate for calculation of the failrate
            df = pd.DataFrame(active_user_habits, columns=['habit_id', 'habit_name', 'starting_date', 'last_check', 'update_expiry','streak', 'interval', 'status','target'])

            # Count how many of each habit exist 
            habit_counts = df['habit_name'].value_counts()
                
            # Create a bar chart of the habit counts
            plt.bar(habit_counts.index, habit_counts.values)

            # Add labels and title to the chart
            plt.xlabel('Habit Name')
            plt.ylabel('Count')
            plt.title('Number of Habit Activations')

            # Display the chart
            plt.show()

        elif analysis == self.option_3:
            ''' This option should show all the active habits where a goal_streak(target) was set and should show
            how far the user is away from completion regarding the current streak in percent'''

            # Get all records from the active habits table (only the ones where status="in progress" are needed)
            active_user_habits = self.db.get_all_active_habits(user_ID)

            # Create a pandas dataframe for all active habits
            df = pd.DataFrame(active_user_habits, columns=['habit_id', 'habit_name', 'starting_date', 'last_check', 'update_expiry','streak', 'interval', 'status','target'])
            
            # Filter only the records with a active streak target
            df_with_target = df[(df['status'] == 'in progress') & (df['target'].notnull())].copy()

            # Calculate the percentage of completion for each habit
            df_with_target.loc[:, 'percent_complete'] = df_with_target['streak'] / df_with_target['target'] * 100

            # Plot the percentage of completion for each habit using a bar chart
            plt.barh(df_with_target['habit_name'], df_with_target['percent_complete'])
            plt.ylabel('Active Habit')
            plt.xlabel('Percent Complete in % from 100%')
            plt.title('Degree of fulfilment active habits with targets')
            
            # Add actual values of each bar inside the bar
            for i, v in enumerate(df_with_target['percent_complete']):
                plt.text(v + 1, i, f"{v:.2f}%", color='black', fontsize=8, va='center')

            # Set x axis to 0-100
            plt.xlim(0,100)

            plt.show()

        elif analysis == self.option_4:
            ''' This option should show all the active habits where a goal_streak(target) was set and should show
            how far the user is away from completion regarding the current streak'''

            # Get all records from the active habits table (only the ones where status="in progress" are needed)
            active_user_habits = self.db.get_all_active_habits(user_ID)

            # Create a pandas dataframe for all active habits
            df = pd.DataFrame(active_user_habits, columns=['habit_id', 'habit_name', 'starting_date', 'last_check', 'update_expiry','streak', 'interval', 'status','target'])
            
            # Filter only the records with a active streak target
            df_with_target = df[(df['status'] == 'in progress') & (df['target'].notnull())]

            # Create a new dataframe with just the habit name, current streak, and target
            df_plot = df_with_target[['habit_name', 'streak', 'target']]

            # Plot the current streak and target for each habit using a stacked bar chart
            ax = df_plot.plot.bar(x='habit_name', stacked=True, rot=0)
            ax.set_xlabel('Habit')
            ax.set_ylabel('Streak/Target')
            ax.set_title('Habit Streaks vs. Targets')
            plt.show()
        
        else:
            print("Other choice")

    # Function for the MyHabits button. 
    def open_highscores(self):
        """
        Opens a new window displaying highscores for different analysis options.
        
        This function creates a new window with a label prompting the user to select a highscore option from a dropdown menu. 
        The selected option is stored in a StringVar object. The function also creates a button to update the highscore table when the option is selected.

        Returns:
            None.

        Raises:
            None.

        Usage:
            Call this function when the "MyHabits" button is clicked.
        """
        
        # Create a new window
        self.highscore_popup = tk.Toplevel(self)
        self.highscore_popup.title("Highscores")
        self.highscore_popup.geometry("800x400")
        self.highscore_popup.grab_set() # Disables interaction with parent window

        # Create a Label with a question
        Label_1 = tk.Label(self.highscore_popup, text='Which highscore do you want to see? Please choose one: ')
        Label_1.pack()
        
        # Define the different possible analysis
        self.highscore_1 = "Longest global streaks" # Shows 
        self.highscore_2 = "Most points earned" # Shows a ranking with the habit tracker points
        self.highscore_3 = "" # 
        self.highscore_4 = "" # 
        dropdown_options = {1: self.highscore_1, 2: self.highscore_2, 3: self.highscore_3, 4: self.highscore_4}

        # Create a StringVar to store the selected option
        self.selected_option = tk.StringVar(self.highscore_popup, self.highscore_1)

        # Create Dropdown menu for choosing predefined highscore options
        highscore_dropdown = tk.OptionMenu(self.highscore_popup, self.selected_option, self.highscore_1, self.highscore_2, self.highscore_3, self.highscore_4)
        highscore_dropdown.pack()

        # Button to update the table
        update_button = tk.Button(self.highscore_popup, text="Update Table", command=self.update_highscore_table)
        update_button.pack()

    def update_highscore_table(self):
        """
        Updates the highscore table depending on the user's selected option. 

        If the user selects option 1, the function prompts the user to enter a monitoring interval (daily, weekly, or monthly). 
        It then gets all active habits for the selected user and sorts them by the decreasing streak. If there are no active habits, 
        it displays a message to the user. Otherwise, it creates a Treeview widget for the longest active streaks and populates it 
        with the relevant data.

        If the user selects option 2, the function gets all active habits for the selected user and calculates points for each habit 
        based on its current streak and interval type (1 point for daily habits, 2 points for weekly habits, and 3 points for monthly habits). 
        It then creates a Pandas DataFrame from the list of active habits and points, groups the data by username, and sums the points 
        for each user. Finally, it creates a Treeview widget for the global points ranking and populates it with the relevant data.
        """
        # First check if treeview widgets exits and if so destroy it. This prevents overlapping.
        for child in self.highscore_popup.winfo_children():
            if isinstance(child, ttk.Treeview):
                child.destroy()
        
        # Get selected option from user 
        highscore_option = self.selected_option.get()
        user_ID = self.user_ID
        # Depending on users choice a specific table opens
        if highscore_option == self.highscore_1:
            # Let the user choose which monitoring interval he wants to see
            interval = simpledialog.askstring("Monitoring Interval", "Enter the monitoring interval you want to see (daily, weekly, or monthly):")
                
            if interval == "daily":    
                interval_ID = 1
            elif interval == "weekly":
                interval_ID = 2
            elif interval == "monthly":
                interval_ID = 3
            else:
                messagebox.showerror("Error", "Please choose either daily, weekly or monthly")
                # Get all active habits and sort them by the streak decreasing
            all_active_user_habits = self.db.get_global_active_habits(interval_ID)
            # If no habits active
            if not all_active_user_habits:
                # Display a message to the user if no active habits/streaks to display
                message_label = tk.Label(frame, text="No habits/streaks to display")
                message_label.pack()
            else:
                # Create a Treeview Widget for the longest active streaks
                self.highscore_1_tree = ttk.Treeview(self.highscore_popup)
                self.highscore_1_tree.place(x = 50, y = 150)
                
                frame = tk.Frame(self.highscore_popup)
                frame.pack(padx=20, pady=20)
                
                # Define Columns
                self.highscore_1_tree['columns'] = ("Rank","Username","Habit Name","Streak", "Interval","Status","Starting Date")

                # Format Columns
                self.highscore_1_tree.column("#0", width=0, minwidth=0) # Remove Ghost column
                self.highscore_1_tree.column("Rank", width=70, minwidth=25)
                self.highscore_1_tree.column("Username", anchor="w", width=100, minwidth=60)                   
                self.highscore_1_tree.column("Habit Name", anchor="w", width=100, minwidth=60)
                self.highscore_1_tree.column("Streak", anchor="center", width=50,minwidth=50)
                self.highscore_1_tree.column("Interval", anchor="w", width=60,minwidth=60)
                self.highscore_1_tree.column("Status", anchor="center", width=100,minwidth=25)
                self.highscore_1_tree.column("Starting Date", anchor="w", width=150,minwidth=50)
                
                # Create Headings
                self.highscore_1_tree.heading("#0",text="",anchor="w") # Remove Ghost column
                self.highscore_1_tree.heading("Rank",text="Rank no. ",anchor="w")
                self.highscore_1_tree.heading("Username",text="Habit Name", anchor="w")
                self.highscore_1_tree.heading("Habit Name",text="Habit Name", anchor="w")
                self.highscore_1_tree.heading("Streak",text="Streak",anchor="center")
                self.highscore_1_tree.heading("Interval",text="Interval",anchor="w")
                self.highscore_1_tree.heading("Status",text="Status",anchor="center")
                self.highscore_1_tree.heading("Starting Date",text="Starting Date",anchor="w")
                
                # Set a counter for inserting records
                counter = 0

                for record in all_active_user_habits:
                    counter +=1
                    item = self.highscore_1_tree.insert(parent="",index="end",iid = counter,text = "", values = (counter,record[8],record[1], record[5], record[6], record[7],record[2]))
        
        # Highscore Option 2. Global points ranking. Depending on the active streaks users can earn points.
        # 1 Point for every streak of daily habits, 2 points for weekly habit streaks and 3 point for every monthly streak
        elif highscore_option == self.highscore_2:
                # Get all active habits for the selected user
            all_active_user_habits = self.db.get_global_active_habits(1) + self.db.get_global_active_habits(2) + self.db.get_global_active_habits(3)

            # Calculate points for each active habit based on its current streak and interval type
            active_habits_points = []
            for habit in all_active_user_habits:
                active_habit_ID = habit[0]
                interval_type = habit[6]
                streak = habit[5]
                username = habit[8]
                if interval_type == 'daily':
                    points = streak
                elif interval_type == 'weekly':
                    points = streak * 2
                elif interval_type == 'monthly':
                    points = streak * 3
                active_habits_points.append((active_habit_ID, username, points))

            # create a dataframe from the list 
            df = pd.DataFrame(active_habits_points, columns=['active_habit_ID', 'username', 'points'])

            # group by username and sum the points
            total_points_df = df.groupby('username').sum().reset_index()

            # sort by total points in descending order
            total_points_df = total_points_df.sort_values('points', ascending=True)

            # create a horizontal bar chart for visualization
            plt.barh(total_points_df['username'], total_points_df['points'], color = "blue")

            # set the chart title and axis labels
            plt.title('Total Points by User')
            plt.xlabel('User')
            plt.ylabel('Points')

            # Add actual values of each bar inside the bar
            for i, v in enumerate(total_points_df['points']):
                plt.text(v + 1, i, f"{v:.2f} Points", color='black', fontsize=8, va='center')

            # display the chart
            plt.show()
