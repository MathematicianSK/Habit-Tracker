from class_habit import Habit


def ordered_list_all_habits(list_habits):
    """Function which gives back a list of all habits, ordered based on their date of creation."""
    return sorted(list_habits, key = lambda h: h.habit_creation_ts, reverse = True)


def ordered_list_all_daily_habits(list_habits):
    """Function which gives back a list of all daily habits (habit_periodicity = 1), ordered based on their date of creation."""
    list_daily_habits = filter(lambda h: h.habit_periodicity == 1, list_habits)
    return sorted(list_daily_habits, key = lambda h: h.habit_creation_ts, reverse = True)


def ordered_list_all_weekly_habits(list_habits):
    """Function which gives back a list of all weekly habits (habit_periodicity = 2), ordered based on their date of creation."""
    list_weekly_habits = filter(lambda h: h.habit_periodicity == 2, list_habits)
    return sorted(list_weekly_habits, key = lambda h: h.habit_creation_ts, reverse = True)


def ordered_list_streaks(list_streaks):
    """Function which gives back a list of the lengths of all streaks of one habit, ordered based on their sizes."""
    list_streaks.sort(key = lambda i: (i[0], i[1]), reverse = True)
    return list_streaks


def longest_streak_habit(list_streaks):
    """Function which gives back the largest length of all streaks of one habit."""
    if len(list_streaks) == 0:
        return 0
    ordered_list_of_streaks = sorted(list_streaks, reverse = True)
    largest_streak = ordered_list_of_streaks[0]
    return largest_streak


def average_streak_length(list_streaks):
    """Function which gives back the average length of the streaks of one habit."""
    length_list = len(list_streaks)
    if length_list == 0:
        return 0.0
    sum_streaks = sum(list_streaks)
    average_streak = sum_streaks / length_list
    return average_streak


def ratio_streaks(list_streaks, sum_intervals):
    """Function which gives back the ratio r = p/q of executed checks p to the maximal amount q of possible checks in the observed time frame for one habit."""
    sum_streaks = sum(list_streaks)
    ratio = sum_streaks / sum_intervals
    return ratio