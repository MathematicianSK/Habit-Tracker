import sys
from datetime import datetime
from class_habit import Habit
from class_habitsstorage import HabitsStorage
import streak
import statistics




habit_state = None




def main_menu():
    """Structure defining code for the CLI of the habit tracker program."""
    print("""Welcome to your habit tracker. You can choose from the following options to work on your routines: 
    1) Check-off a habit 
    2) Create a habit 
    3) Remove a habit 
    4) Statistics 
    """)
    try:
        user_input = int(input("Type in a number: "))
    except(EOFError, KeyboardInterrupt):
        print("Abortion!")
        return
    if user_input == 1:
        check_off_habit_sub_menu()
    elif user_input == 2:
        add_habit_sub_menu()
    elif user_input == 3:
        remove_habit_sub_menu()
    elif user_input == 4:
        statistics_sub_menu()
    else:
        print(user_input, " is not a valid option!")




def check_off_habit_sub_menu():
    """Structure defining code for the sub menu to check-off a habit."""
    # Determining the current date for a timestamp. 
    check_off_date = datetime.now().astimezone()
    print("""Here are all your habits you can check-off: """)
    # Determining all habits which are not checked-off so far and put them in a list. 
    list_unchecked_habits = []
    for habit in habit_state.list_all_habits():
        list_checks = habit_state.list_all_checks(habit.habit_id)
        # If a habit has not been checke-off so far (so that the list of checks is empty), 
        # then add the habit to the list. 
        if len(list_checks) == 0:
            list_unchecked_habits.append(habit)
            continue
        # Determining the time interval indices of the time interval which includes the current time 
        # and the time interval which includes the last check-off.
        habit_duration = index_periodicity_in_seconds(habit.habit_periodicity)
        current_interval_index = streak.time_interval_index(generate_timestamp(), habit_duration)
        latest_check_index = streak.time_interval_index(list_checks[-1], habit_duration)
        # If the two indices are not identical, add the habit to the list of unchecked habits 
        # because there is no index of a check-off with the index of the current time. 
        if current_interval_index != latest_check_index:
            list_unchecked_habits.append(habit)
    # Give out the list of all unchecked habits with their corresponding habit-IDs. 
    for habit in list_unchecked_habits:
        print(f"{habit.habit_id:4} | {habit.habit_name}")
    try:
        habit_id = input("Type in a habit-ID to check-off the corresponding habit: ")
        habit_check_off(habit_id)
    except (EOFError, KeyboardInterrupt):
        print(f"Your typed in habit-ID '{habit_id}' is not valid! Try again!")
        quit()




def add_habit_sub_menu():
    """Structure defining code for the sub menu to add a habit."""
    print("""Here you can create a new habit. 
If you want to generate a habit with a daily periodicity, type in 1, 
if you want to add a habit with a a weekly periodicity, type in 2.""")
    try:
        habit_periodicity = int(input("Type in the number: "))
        habit_name = input("You can now type in the name of your new habit: ")
        habit_add(habit_name, habit_periodicity)
    except (EOFError, KeyboardInterrupt):
        print("Abort!")
        return




def remove_habit_sub_menu():
    """Structure defining code for the sub menu to remove a habit."""
    print("""Here are all the habits which exist in your list: """)
    # Printing all habits with their corresponding habit-IDs. 
    for habit in habit_state.list_all_habits():
        print(f"{habit.habit_id:4} | {habit.habit_name}")
    try:
        habit_id = input("Type in a habit-ID to remove the corresponding habit: ")
        habit_remove(habit_id)
    except (EOFError, KeyboardInterrupt):
        print("Abort!")
        return




def statistics_sub_menu():
    """Structure defining code for the sub menu of the statistics section."""
    print("""You have the following options to analyse your habits: 
    1) List of all habits 
    2) List of all daily habits 
    3) List of all weekly habits 
    4) Ordered list of the longest streaks of each habit 
    5) Ordered list of the average streak length of each habit 
    6) Ordered list of the check-off ratio of each habit 
    7) Ordered list of all streaks of a chosen habit 
    """)
    try: 
        user_input_statistics = int(input("Type in a number: "))
    except(EOFError, KeyboardInterrupt):
        print("Abortion!")
        return
    if user_input_statistics == 1: 
        ordered_list_all_habits()
    elif user_input_statistics == 2: 
        ordered_list_daily_habits()
    elif user_input_statistics == 3: 
        ordered_list_weekly_habits()
    elif user_input_statistics == 4: 
        ordered_list_longest_streaks_each_habit()
    elif user_input_statistics == 5: 
        ordered_list_average_streaks_each_habit()
    elif user_input_statistics == 6: 
        ordered_list_check_off_ratio_each_habit()
    elif user_input_statistics == 7: 
        streaks_sub_sub_menu()
    else:
        print(user_input_statistics, " is not a valid option!")




def streaks_sub_sub_menu():
    """Structure defining code for the sub-sub menu to receive the ordered list of all streaks of a chosen habit."""
    print("""Here are all the habits which exist in your list: """)
    # Printing all habits with their corresponding habit-IDs.
    for habit in habit_state.list_all_habits():
        print(f"{habit.habit_id:4} | {habit.habit_name}")
    try:
        habit_id = input("Type in a habit-ID to show the ordered list of all streaks the corresponding habit: ")
        ordered_list_streaks_one_habit(habit_id)
    except (EOFError, KeyboardInterrupt):
        print("Abort!")
        return




def generate_timestamp():
    """Function which gives back the current time to create a timestamp."""
    return int(datetime.now().timestamp())




def index_periodicity_in_seconds(interval_index: int):
    if interval_index == 1:
        # Length of a day in seconds: 24x60x60 = 86400
        return 86400
    elif interval_index == 2:
        # Length of a week in seconds: 7x24x60x60 = 604800
        return 604800
    else:
        raise IndexError(f"The number '{interval_index}' does not represent a valid time interval!")




def habit_check_off(habit_id):
    """Function which checks-off a chosen habit (defined by its habit-ID) by using the \"check_habit\" attibute from \"Class HabitsStorage\".""" 
    try:
        # Asking for the habit-ID and then put a new timestamp in the list of checks of the corresponding habit.
        habit_id = int(habit_id)
        habit_state.check_habit(habit_id, generate_timestamp())
    except ValueError:
        print(f"The typed in number '{habit_id}' is not an existing habit-ID!")
    except KeyError as e:
        print(f"Id error: {e}.")




def habit_add(habit_name, habit_periodicity):
    """Function which creates a habit in the JSON file by using the \"add_habit\" attibute from \"Class HabitsStorage\"."""
    try:
        # Asking for the name of the habit. If you did not put in a name (= 0 letters), you get an error. 
        habit_name = habit_name.strip()
        if len(habit_name) == 0:
            print("You did not give a name. Try again!")
            quit()
        # Asking for the periodicity of the habit (1 = daily, 2 = weekly). 
        # If you did not type in the numbers 1 or 2, you get an error. 
        habit_periodicity = int(habit_periodicity)
        if habit_periodicity != 1 and habit_periodicity != 2:
            print(f"The integer '{habit_periodicity}' you gave is not valid! The integer you put in must be either 1 for a daily periodicity or 2 for a weekly periodicity!")
            quit()
        # Creating the habit and storing it in the JSON file. 
        habit = Habit(habit_id = None, habit_name = habit_name, habit_periodicity = habit_periodicity, habit_creation_ts = generate_timestamp())
        habit_state.add_habit(habit)
        print(f"You added the new habit '{habit.habit_name}' to the list.")
    except ValueError:
        print(f"The number '{habit_periodicity}' you gave is not valid! The integer you put in must be either 1 for a daily periodicity or 2 for a weekly periodicity!")
        quit()
    except KeyError as e:
        print(e)
        quit()




def habit_remove(habit_id):
    """Function which removes a habit from the JSON file by using the \"remove_habit\" attibute from \"Class HabitsStorage\"."""
    try:
        # Asking for the habit-ID and then removing the corresponding habit from the JSON file. 
        habit_id = int(habit_id)
        habit_state_remove_habit(habit_id)
        print(f"You removed the habit with the habit-ID '{habit_id}'!")
    except ValueError:
        print(f"The chosen habit-ID '{habit_id}' is not a number!")
        quit()
    except KeyError as e:
        print(e, "Do nothing ....")
        quit()




def ordered_list_all_habits():
    """Function which gives back the list of all tracked habits with their date of creation, ordered based on this date."""
    print("Here are all your tracked habits and their date of creation:")
    # Retrieving all habits and ordering them based on their date of creation. 
    list_habits = habit_state.list_all_habits()
    ordered_all_habits = statistics.ordered_list_all_habits(list_habits)
    # Asking for the time of creation and then giving out the list. 
    for habit in ordered_all_habits:
        date_string = datetime.fromtimestamp(habit.habit_creation_ts).astimezone()
        print(f"{habit.habit_name} | {date_string}")




def ordered_list_daily_habits():
    """Function which gives back the list of all tracked daily habits with their date of creation, ordered based on this date."""
    print("Here are all your tracked daily habits and their date of creation:")
    # Retrieving all habits and then ordering all the daily ones based on their date of creation. 
    list_habits = habit_state.list_all_habits()
    ordered_all_daily_habits = statistics.ordered_list_all_daily_habits(list_habits)
    # Asking for the time of creation and then giving out the list. 
    for habit in ordered_all_daily_habits:
        date_string = datetime.fromtimestamp(habit.habit_creation_ts).astimezone()
        print(f"{habit.habit_name} | {date_string}")




def ordered_list_weekly_habits():
    """Function which gives back the list of all tracked weekly habits with their date of creation, ordered based on this date."""
    print("Here are all your tracked weekly habits and their date of creation:")
    # Retrieving all habits and then ordering all the weekly ones based on their date of creation. 
    list_habits = habit_state.list_all_habits()
    ordered_all_weekly_habits = statistics.ordered_list_all_weekly_habits(list_habits)
    # Asking for the time of creation and then giving out the list. 
    for habit in ordered_all_weekly_habits:
        date_string = datetime.fromtimestamp(habit.habit_creation_ts).astimezone()
        print(f"{habit.habit_name} | {date_string}")




def ordered_list_longest_streaks_each_habit():
    """Function which gives back an ordered list of the largest streak lengths for each tracked habit."""
    print("Here are the largest streak lengths for each of your tracked habits:")
    # Retrieving all habits. 
    list_habits = habit_state.list_all_habits()
    # Creating a list of every habit with its largest streak length. 
    list_ordered_streaks = []
    for habit in list_habits:
        list_checks = habit_state.list_all_checks(habit.habit_id)
        habit_duration = index_periodicity_in_seconds(habit.habit_periodicity)
        list_streaks = streak.calculate_streak_lengths(list_checks, habit_duration)
        longest_streak = statistics.longest_streak_habit(list_streaks)
        list_ordered_streaks.append((longest_streak, habit.habit_name))
    # Ordering the created list based on the the value of the largest streak lengths and then printing the list. 
    list_ordered_streaks.sort(key = lambda a: a[0], reverse = True)
    for max_streak, name_habit in list_ordered_streaks:
        print(f"{max_streak} | {name_habit}")




def ordered_list_average_streaks_each_habit():
    """Function which gives back an ordered list of the average streak lengths for each tracked habit."""
    print("Here are the average streak lengths for each of your tracked habits:")
    # Retrieving all habits. 
    list_habits = habit_state.list_all_habits()
    # Creating a list of every habit with its average streak length. 
    list_ordered_average_streaks = []
    for habit in list_habits:
        list_checks = habit_state.list_all_checks(habit.habit_id)
        habit_duration = index_periodicity_in_seconds(habit.habit_periodicity)
        list_streaks = streak.calculate_streak_lengths(list_checks, habit_duration)
        average_streak = statistics.average_streak_length(list_streaks)
        list_ordered_average_streaks.append((average_streak, habit.habit_name))
    # Ordering the created list based on the the value of the average streak lengths and then printing the list. 
    list_ordered_average_streaks.sort(key = lambda a: a[0], reverse = True)
    for avg_streak, name_habit in list_ordered_average_streaks:
        print(f"{avg_streak:9.4} | {name_habit}")




def ordered_list_check_off_ratio_each_habit():
    """Function which gives back an ordered list of the check-off ratios for each tracked habit. \n 
    The check-off ratio is the fraction r = p/q of executed checks p to the maximal amount q of possible checks in the observed time frame for one habit."""
    print("Here are the check-off ratios for each of your tracked habits:")
    # Retrieving all habits. 
    list_habits = habit_state.list_all_habits()
    # Creating a list of every habit with its check-off ratio. 
    list_ordered_ratios = []
    for habit in list_habits:
        list_checks = habit_state.list_all_checks(habit.habit_id)
        habit_duration = index_periodicity_in_seconds(habit.habit_periodicity)
        list_streaks = streak.calculate_streak_lengths(list_checks, habit_duration)
        habit_duration = index_periodicity_in_seconds(habit.habit_periodicity)
        current_interval_index = streak.time_interval_index(generate_timestamp(), habit_duration)
        creation_check_index = streak.time_interval_index(habit.habit_creation_ts, habit_duration)
        index_difference = current_interval_index - creation_check_index + 1
        ratio_check_off = statistics.ratio_streaks(list_streaks, index_difference)
        list_ordered_ratios.append((ratio_check_off, habit.habit_name))
    # Ordering the created list based on the the value of the check-off ratios and then printing the list. 
    list_ordered_ratios.sort(key = lambda a: a[0], reverse = True)
    for max_ratio, name_habit in list_ordered_ratios:
        print(f"{max_ratio} | {name_habit}")




def ordered_list_streaks_one_habit(habit_id):
    """Function which gives back an ordered list of all the streaks with their start and end date for a chosen habit."""
    # Retrieving all habits. 
    habit = habit_state.retrieve_habit(habit_id)
    # Generating the list of the lengths of all streaks of a habit and their beginning and end dates. 
    list_checks = habit_state.list_all_checks(habit.habit_id)
    habit_duration = index_periodicity_in_seconds(habit.habit_periodicity)
    list_streaks = streak.return_streak_lengths_and_dates(list_checks, habit_duration)
    # Ordering the created based on the values of the lengths and then printing the list. 
    ordered_list_streaks = statistics.ordered_list_streaks(list_streaks)
    print(f"The streaks of '{habit.habit_name}' are:")
    for element_streak, start_ts, end_ts in ordered_list_streaks:
        start_date = datetime.fromtimestamp(start_ts).astimezone()
        end_date = datetime.fromtimestamp(end_ts).astimezone()
        print(f"{element_streak} | {start_date} - {end_date}")
        
    


if __name__ == "__main__":
    habit_state = HabitsStorage("habitfile.json")
    main_menu()