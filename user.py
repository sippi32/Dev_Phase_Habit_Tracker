import tkinter as tk
import datetime as dt
import time
from habit import Habit
from database import MySQLDatabase 


class User:
    def __init__(self, first_name, last_name, username, password, email, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.phone_number = str(phone_number)
        self.created_time =  dt.datetime.now()
        self.last_update = self.created_time

    def __repr__(self):
        return f"User username = {self.username}, first_name = {self.first_name}, last_name = {self.last_name}, password = {self.password}, email = {self.email}, phone_number = {self.phone_number}, created_time = {self.created_time}, last_update = {self.last_update})"


    def update_profile(self, new_first_name=None, new_last_name=None, new_username=None, new_password=None, new_email=None, new_phone_number=None):
        if new_first_name:
            self.first_name = new_first_name
        if new_last_name:
            self.last_name = new_last_name          
        if new_username:
            self.username = new_username
        if new_password:
            self.password = new_password
        if new_email:
            self.email = new_email
        if new_phone_number:
            self.email = new_email
        self.last_update = dt.datetime.now()


    # def create_habit(self, habit_name, username, category_ID):
    #     user_ID = self.db.get_userID(username)
    #     description = "stop smoking"
        
    #     new_habit = Habit(habit_name, user_ID, category_ID, description )
    #     #return new_habit
    #     # Preparation of dictionary for insert_data function from MySQLDatabase class
    #     data = {'habit_name': habit_name, 'user_ID': user_ID, 'category_ID': category_ID, 'description': description}     
    #     self.db.insert_data("habits", data)
        




    


        
        





# User.db = MySQLDatabase('localhost','root','Mannheim','marc')

# existing_user = User.load_user("Sippenpit")

# existing_user.create_habit("exercise", "Sippenpit", 1)















# user1 = User("Marc","Fischer","Sippi","asd","asd@wqe.de",2342349234)
# user2 = User("asdasd","Fischer","Sippi","asd","asd@wqe.de",23123123)
# print(user1)
# print(user2)

# time.sleep(10)

# user1.update_profile(new_first_name="Heinz")
# user2.update_profile(new_email='f.marc.1991@web.de', new_phone_number= '122222222')

# print(user1)
# print(user2)
