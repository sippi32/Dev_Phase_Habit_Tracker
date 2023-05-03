import datetime as dt

class User:
    """A class representing a user account.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        username (str): The user's username.
        password (str): The user's password.
        email (str): The user's email address.
        phone_number (str): The user's phone number.
        created_time (datetime): The date and time when the user account was created.
        last_update (datetime): The date and time when the user account was last updated.

    Methods:
        __init__(self, first_name, last_name, username, password, email, phone_number):
            Initializes a new instance of the User class with the given attributes.

        __repr__(self):
            Returns a string representation of the User object.

        update_profile(self, new_first_name=None, new_last_name=None, new_username=None,
                       new_password=None, new_email=None, new_phone_number=None):
            Updates the user's profile with the given attributes.

            Args:
                new_first_name (str, optional): The user's new first name.
                new_last_name (str, optional): The user's new last name.
                new_username (str, optional): The user's new username.
                new_password (str, optional): The user's new password.
                new_email (str, optional): The user's new email address.
                new_phone_number (str, optional): The user's new phone number.

            Returns:
                None
    """
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


        




    


        
        



















