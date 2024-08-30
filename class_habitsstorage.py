import json
from class_habit import Habit

class HabitsStorage(): 
    """Class which defines how the data of a habit is stored and retrieved from a JSON file."""

    # A dictionary to save the data of all habits which contains a dictionary of all the habits and their defining data 
    # as well as a dictionary of all the checks for each habit. 
    habits_checks_dict = {"habits_dict": {}, "checks_dict": {}}

    
    def __init__(self, path):
        self.data = HabitsStorage.habits_checks_dict
        self.max_id = 1
        self.filepath = path
        self.load_habit(path)

    
    def load_habit(self, path: str):
        """Function which creates a JSON file the first time a habit is created (and a file do not exist so far), 
        otherwise defines the filepath for the saving of new data of a habit."""
        
        try:
            # Defining the filepath for saving when the JSON file already exists. 
            with open(path, "r") as read_data:
                self.data = json.load(read_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("The file is not in JSON format, it therefore cannot be saved!")
        # Defining the creation of a JSON file if it does not exist so far. 
        except FileNotFoundError:
            with open(path, "w") as write_data:
                json.dump(HabitsStorage.habits_checks_dict, write_data)
            self.data = HabitsStorage.habits_checks_dict
            self.max_id = 1
            return

        # Checking if all the keys in habits_checks_dict exist. 
        if "habits_dict" not in self.data:
            raise KeyError("The JSON file does not contain a \"habits_dict\" key!")
        if "checks_dict" not in self.data:
            raise KeyError("The JSON file does not contain a \"checks_dict\" key!")
        
        # Checking if the values of all the keys are of the right data type. 
        if not isinstance(self.data["habits_dict"], dict):
            raise ValueError("The value of \"habits_dict\" is not a dictionary type!")
        if not isinstance(self.data["checks_dict"], dict):
            raise ValueError("The value of \"checks_dict\" is not a dictionary type!")

        # Checking if checks_dict has an existing habit_id.
        for habit_id in self.data["checks_dict"]:
            if habit_id not in self.data["habits_dict"]:
                raise KeyError("The not existing habit-ID {habit_id} was found in \"checks_dict\"!")

        # Ordering the timestamp entries of the lists in checks_dict. 
        for entries_checks in self.data["checks_dict"].values():
            entries_checks.sort()

        # Finding the largest habit-ID. 
        self.max_id = max(map(int, self.data["habits_dict"]), default = 0) + 1


    def save_habit(self, path: str):
        """Function which defines how data of a habit is saved in the JSON file."""
        with open(path, "w") as save_data:
            json.dump(self.data, save_data)


    def add_habit(self, habit: Habit):
        """Function which defines how a new habit is added to the JSON file."""
        # Giving the new habit its habit-ID. 
        if habit.habit_id is None:
            habit.habit_id = self.max_id
            self.max_id += 1
        elif str(habit.habit_id) in selfdata["habits_dict"]:
            raise KeyError("The chosen habit-ID already exists!")
        # Loading the habit as a dictionary in the JSON file. 
        self.data["habits_dict"][str(habit.habit_id)] = vars(habit)
        # Saving the new JSON file. 
        self.save_habit(self.filepath)
        return habit.habit_id


    def remove_habit(self, habit_id: int):
        """Function which removes a habit from the JSON file based on its habit-ID."""
        if str(habit_id) not in self.data["habits_dict"]:
            raise KeyError("The chosen habit-ID does not exist!")
        if str(habit_id) in self.data["checks_dict"]:
            del self.data["checks_dict"][str(habit_id)]
        del self.data["habits_dict"][str(habit_id)]
        # Determining the new habit-ID for the next new habit. 
        self.max_id = max(map(int, self.data["habits_dict"]), default = 0) + 1
        # Saving the new JSON file. 
        self.save_habit(self.filepath)


    def retrieve_habit(self, habit_id: int):
        """Function which gives the defining data of a specific habit back based on the habit-ID."""
        if str(habit_id) not in self.data["habits_dict"]:
            raise KeyError("The chosen habit-ID does not exist!")
        return Habit(**self.data["habits_dict"][str(habit_id)])


    def list_all_habits(self):
        """Gives a list of all tracked habits back in their current state."""
        habits_list = []
        for habit_data in self.data["habits_dict"].values():
            habits_list.append(Habit(**habit_data))
        return habits_list


    def check_habit(self, habit_id: int, timestamp: int):
        """Function which adds a new timestamp in the checks dictionary for a new check of the corresponding habit."""
        if str(habit_id) not in self.data["habits_dict"]:
            raise KeyError("The chosen habit-ID does not exist!")
        timestamp = int(timestamp)
        # Create a list for checks (with the current check as the first entry) if it does not exist so far. 
        if str(habit_id) not in self.data["checks_dict"] or len(self.data["checks_dict"][str(habit_id)]) < 1:
            self.data["checks_dict"][str(habit_id)] = [timestamp]
        # Add the timestamp to the existing list. 
        else:
            self.data["checks_dict"][str(habit_id)].append(timestamp)
            # Ordering the list of timestamps. 
            if self.data["checks_dict"][str(habit_id)][-2] > timestamp:
                self.data["checks_dict"][str(habit_id)].sort()
        # Saving the new JSON file. 
        self.save_habit(self.filepath)


    def list_all_checks(self, habit_id: int):
        """Function which gives a list of all the checks of a particular habit."""
        if str(habit_id) not in self.data["habits_dict"]:
            raise KeyError("The chosen habit-ID does not exist!")
        if str(habit_id) not in self.data["checks_dict"]:
            return []
        return self.data["checks_dict"][str(habit_id)]