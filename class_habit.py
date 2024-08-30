from dataclasses import dataclass
from datetime import datetime

@dataclass
class Habit:
    """Class which states the attributes to define a habit and makes it therefore possible to track this habit-item in the program."""

    # An integer as an identification number to uniquely mark a habit
    habit_id: int 
    # String for the name of a habit
    habit_name: str 
    # Integer which represents the periodicity (daily or weekly) of a tracked habit
    habit_periodicity: int 
    # A integer-timestamp which gives the time of the creation of a habit
    habit_creation_ts: int = int(datetime.now().timestamp())

    def __str__(self):
        """A function in string format to give a timestamp in a human readable form."""
        timestamp_rep = datetime.fromtimestamp(habit_creation_ts).astimezone()
        if self.habit_periodicity == 1: 
            habit_period = "daily"
        if self.habit_periodicity == 2:
            habit_period = "weekly"
        else: 
            raise ValueError("Invalid index for the periodicity of a habit!")
        return f"{self.habit_id}: '{self.habit_name}' with a {habit_period} periodicity, created at {timestamp_rep}."