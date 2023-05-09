import datetime
from database import MySQLDatabase


class Habit:
    """
    A class representing a user's habit.

    Attributes:
    - habit_name (str): The name of the habit.
    - user_ID (int): The ID of the user who created the habit.
    - category_ID (int): The ID of the category the habit belongs to.
    - creation_date (str): The date the habit was created.
    - description (str): Optional description of the habit.

    Methods:
    - __repr__(self): Returns a string representation of the Habit object.
    - create_dict(self): Returns a dictionary of the habit object.
    """
    
    def __init__(self, habit_name, user_ID, category_ID, description = None, creation_date = None):
        self.habit_name = habit_name
        self.user_ID = user_ID
        self.category_ID = category_ID
        self.creation_date = creation_date if creation_date is not None else datetime.datetime.now().isoformat()
        self.description = description

    def __repr__(self):
        """Returns a string representation of the habit object.

        Returns:
            str: A string representation of the habit object, in the format (habit_name, user_ID, category_ID, creation_date, description).
        """
        return f"({self.habit_name}, {self.user_ID}, {self.category_ID}, {self.creation_date}, {self.description})"       

    # Function to create a dictionary with habit attributes  
    def create_dict(self):
        habit_name = self.habit_name
        user_ID = self.user_ID
        category_ID = self.category_ID
        description = self.description
        
        dict = {'habit_name': habit_name, 'user_ID': user_ID, 'category_ID': category_ID, 'description': description}

        return dict




        