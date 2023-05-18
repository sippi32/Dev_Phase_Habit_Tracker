import datetime as dt

class ActiveUserHabit:
    """
    Represents a habit being tracked by a user.

    Attributes:
        user_ID (int): The ID of the user who is tracking the habit.
        habit_ID (int): The ID of the habit being tracked.
        interval_ID (int): The ID of the interval in which the habit is being tracked.
        starting_date (datetime): The date and time when the user started tracking the habit.
        last_check (datetime): The date and time when the user last checked off the habit.
        update_expiry (datetime): The date and time when the user's habit streak will expire if they do not check it off.
        streak (int): The number of consecutive days/weeks/months the user has checked off the habit.
        status (str): The current status of the habit ('in progress', 'completed', or 'failed').
        goal_streak (int): The number of consecutive days/ weeks/ months the user is aiming to check off the habit.
        end_date (datetime): The date and time when the user plans to stop tracking the habit.
    """
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
        """
        Returns a string representation of the ActiveUserHabit object.

        Returns:
        str: A string containing the values of the object's attributes.
        """
        return f"ActiveUserHabit user_ID={self.user_ID}, habit_ID={self.habit_ID}, interval_ID={self.interval_ID}, starting_date={self.starting_date}, last_check={self.last_check}, update_expiry={self.update_expiry}, streak={self.streak}, goal_streak={self.goal_streak}, status={self.status}, end_date={self.end_date}"


 



