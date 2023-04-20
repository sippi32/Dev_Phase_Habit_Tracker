import datetime


class Habit:
    def __init__(self, habit_name, user_ID, category_ID, description = None, creation_date = None):
        self.habit_name = habit_name
        self.user_ID = user_ID
        self.category_ID = category_ID
        self.creation_date = creation_date if creation_date is not None else datetime.datetime.now().isoformat()
        self.description = description

     
    def __repr__(self):
        return f"({self.habit_name}, {self.user_ID}, {self.category_ID}, {self.creation_date}, {self.description})"       
        

        
        




        