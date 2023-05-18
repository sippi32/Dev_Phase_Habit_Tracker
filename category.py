import datetime

class Category:
    """A class representing a category for habits.

    Attributes:
        category_name (str): The name of the category.
        user_ID (int): The ID of the user who created the category.
        description (str, optional): A brief description of the category. Defaults to None.
        creation_date (str, optional): The date and time when the category was created, in ISO format. Defaults to the current date and time.

    Methods:
        __repr__: Returns a string representation of the category object.
        create_dict: Returns a dictionary
    """
    def __init__(self, category_name, user_ID, description = None, creation_date = None):
        self.category_name = category_name
        self.user_ID = user_ID
        self.creation_date = creation_date if creation_date is not None else datetime.datetime.now().isoformat()
        self.description = description

     
    def __repr__(self):
        """Returns a string representation of the category object.

        Returns:
            str: A string representation of the category object, in the format (category_name, user_ID, creation_date, description).
        """
        return f"({self.category_name}, {self.user_ID},{self.creation_date}, {self.description})"       
        
    # Function to create a dictionary with category attributes  
    def create_dict(self):
        category_name = self.category_name
        user_ID = self.user_ID
        creation_date = self.creation_date
        description = self.description
        
        dict = {'category_name': category_name, 'user_ID': user_ID, 'creation_date': creation_date, 'description': description}

        return dict

