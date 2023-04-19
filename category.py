import datetime


class Category:
    def __init__(self, category_name, user_ID, description = None, creation_date = None):
        self.category_name = category_name
        self.user_ID = user_ID
        self.creation_date = creation_date if creation_date is not None else datetime.datetime.now().isoformat()
        self.description = description

     
    def __repr__(self):
        return f"({self.category_name}, {self.user_ID},{self.creation_date}, {self.description})"       
        
