from database import MySQLDatabase
import datetime as dt
from user import User
from habit import Habit
from category import Category



class ActiveUserHabit:
    def __init__(self, user_ID, habit_ID, interval_ID, goal_streak=None, end_date=None, last_check=None, update_expiry=None):
        self.user_ID = user_ID
        self.habit_ID = habit_ID
        self.interval_ID = interval_ID
        self.starting_date = dt.datetime.now()
        self.last_check = last_check
        self.update_expiry = update_expiry
        self.streak = 0
        self.status = 'in progress'
        self.goal_streak = goal_streak
        self.end_date = end_date


    def __repr__(self):
        return f"ActiveUserHabit user_ID = {self.user_ID}, habit_ID = {self.habit_ID}, interval_ID = {self.interval_ID}, starting_date = {self.starting_date}, last_check = {self.last_check}, update_expiry = {self.update_expiry}, streak = {self.streak}, goal_streak = {self.goal_streak}, status = {self.status}, end_date = {self.end_date}"


 



# active1 = ActiveUserHabit(1,2,3,40)

# print(repr(active1))