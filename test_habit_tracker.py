import pytest
from datetime import datetime
from class_habit import Habit
from class_habitsstorage import HabitsStorage
import streak
import statistics




@pytest.fixture
def full_test_data(tmp_path_factory):
    file_path = tmp_path_factory.mktemp("testdata") / "example_data_habit_tracker.json"
    with open(file_path, "w") as f:
        f.write(
            """{
        "habits_dict": {
            "1":  {"habit_id": 1, "habit_name": "Take your medicine!",         "habit_periodicity": 1, "habit_creation_ts": 1719326209}, 
            "2":  {"habit_id": 2, "habit_name": "Water your plants!",          "habit_periodicity": 2, "habit_creation_ts": 1719419861}, 
            "3":  {"habit_id": 3, "habit_name": "Did you do overtime?",        "habit_periodicity": 1, "habit_creation_ts": 1719420210}, 
            "4":  {"habit_id": 4, "habit_name": "Weekly phonecalls",           "habit_periodicity": 2, "habit_creation_ts": 1719419872}, 
            "5":  {"habit_id": 5, "habit_name": "Go for a walk with the dog!", "habit_periodicity": 1, "habit_creation_ts": 1719418096}
        },
        "checks_dict": {
            "1": [
                   1719792657, 1719902537, 1720002330, 1720109000, 1720166824, 1720294049, 1720339217, 1720466165, 1720528630, 1720625203, 1720657298, 1720781229, 1720853778, 1720976382,                            1721019025, 1721108813, 1721177695, 1721260957, 1721379416, 1721474265, 1721549695, 1721660653, 1721760880, 1721837214, 1721913230, 1721982123, 1722104546, 1722176684,                            1722270549, 1722368364, 1722447574
            ],
            "2": [1719420821], 
            "3": [
                   1719792657, 1719902537, 1720002330, 1720109000,
                   1720294049, 1720339217, 1720466165, 1720528630, 1720625203, 1720657298, 
                   1720853778, 1720976382, 1721019025, 1721108813, 1721177695, 1721260957, 1721379416, 1721474265, 
                   1721660653, 1721760880, 1721837214, 1721913230, 1721982123, 1722104546, 1722176684, 1722270549, 1722368364, 1722447574 
            ]
        }
    }
    """
        )
    habit_state = HabitsStorage(file_path)
    return habit_state




# Test of Class HabitsStorage: 


def test_all_habit(full_test_data):
    habit_state_example = full_test_data
    habit = Habit(None, "Do math!", 1, 1722462952)
    habit_id_example = habit_state_example.add_habit(habit)
    assert habit_id_example == 6


def test_remove_habit(full_test_data):
    habit_state_example = full_test_data
    list_habit_example = habit_state_example.list_all_habits()
    habit_id_example = 5
    habit_state_example.remove_habit(habit_id_example)
    list_habit_example_new = habit_state_example.list_all_habits()
    assert len(list_habit_example) == len(list_habit_example_new) + 1


def test_retrieve_habit(full_test_data):
    habit_state_example = full_test_data
    habit_id_example = 4
    habit_example = habit_state_example.retrieve_habit(habit_id_example)
    assert habit_example.habit_id == 4


def test_list_all_habits(full_test_data):
    habit_state_example = full_test_data
    list_habit_example = habit_state_example.list_all_habits()
    assert len(list_habit_example) == 5


def test_check_habit(full_test_data):
    habit_state_example = full_test_data
    timestamp = 1720931087
    habit_state_example.check_habit(4, timestamp)
    list_checks_habit_4 = habit_state_example.list_all_checks(4)
    assert len(list_checks_habit_4) == 1
    assert list_checks_habit_4[0] == timestamp


def test_list_all_checks(full_test_data):
    habit_state_example = full_test_data
    list_checks_habit_1 = habit_state_example.list_all_checks(1)
    assert len(list_checks_habit_1) == 31
    



# Test of the module "streak":


def test_time_interval_index(full_test_data):
    habits_state_example = full_test_data
    timestamp = habits_state_example.list_all_checks(1)[5]
    period_length = 86400
    interval_index = streak.time_interval_index(timestamp, period_length)
    assert interval_index > 0


def test_time_interval_boundaries(full_test_data):
    habits_state_example = full_test_data
    timestamp = habits_state_example.list_all_checks(1)[2]
    period_length = 86400
    interval_boundaries = streak.time_interval_boundaries(timestamp, period_length)
    assert interval_boundaries[1] - interval_boundaries[0] == 86400


def test_calculate_streak_lengths(full_test_data):
    habits_state_example = full_test_data
    list_timestamps = habits_state_example.list_all_checks(1)
    period_length = 86400
    list_lengths_streaks = streak.calculate_streak_lengths(list_timestamps, period_length)
    assert len(list_lengths_streaks) == 1
    assert list_lengths_streaks[0] == 31


def test_return_streak_lengths_and_dates(full_test_data):
    habits_state_example = full_test_data
    list_timestamps = habits_state_example.list_all_checks(1)
    period_length = 86400
    list_lengths_and_dates = streak.return_streak_lengths_and_dates(list_timestamps, period_length)
    assert len(list_lengths_and_dates) == 1
    assert list_lengths_and_dates[0][0] == 31




# Test of the module "statistics": 


def test_ordered_list_all_habits(full_test_data):
    habits_state_example = full_test_data
    list_habits_example = habits_state_example.list_all_habits()
    list_ordered_habits_example = statistics.ordered_list_all_habits(list_habits_example)
    assert list_ordered_habits_example[0].habit_creation_ts == 1719420210
    assert list_ordered_habits_example[-1].habit_creation_ts == 1719326209


def test_ordered_list_all_daily_habits(full_test_data):
    habits_state_example = full_test_data
    list_habits_example = habits_state_example.list_all_habits()
    list_ordered_habits_example = statistics.ordered_list_all_daily_habits(list_habits_example)
    assert list_ordered_habits_example[0].habit_creation_ts == 1719420210
    assert list_ordered_habits_example[-1].habit_creation_ts == 1719326209


def test_ordered_list_all_weekly_habits(full_test_data):
    habits_state_example = full_test_data
    list_habits_example = habits_state_example.list_all_habits()
    list_ordered_habits_example = statistics.ordered_list_all_weekly_habits(list_habits_example)
    assert list_ordered_habits_example[0].habit_creation_ts == 1719419872
    assert list_ordered_habits_example[-1].habit_creation_ts == 1719419861


def test_ordered_list_streaks(full_test_data):
    habits_state_example = full_test_data
    list_checks_example = habits_state_example.list_all_checks(3)
    list_streak_lengths_example = streak.return_streak_lengths_and_dates(list_checks_example, 86400)
    longest_streak_length_example = statistics.ordered_list_streaks(list_streak_lengths_example)
    assert len(longest_streak_length_example) == 4
    assert longest_streak_length_example[0][0] == 10


def test_longest_streak_habit(full_test_data):
    habits_state_example = full_test_data
    list_checks_example = habits_state_example.list_all_checks(3)
    list_streak_lengths_example = streak.calculate_streak_lengths(list_checks_example, 86400)
    longest_streak_length_example = statistics.longest_streak_habit(list_streak_lengths_example)
    assert longest_streak_length_example == 10


def test_average_streak_length(full_test_data):
    habits_state_example = full_test_data
    list_checks_example = habits_state_example.list_all_checks(3)
    list_streak_lengths_example = streak.calculate_streak_lengths(list_checks_example, 86400)
    average_streak_length_example = statistics.average_streak_length(list_streak_lengths_example)
    assert abs(average_streak_length_example - 7.0) < 0.0001


def test_ratio_streaks(full_test_data):
    habits_state_example = full_test_data
    list_checks_example = habits_state_example.list_all_checks(3)
    list_streak_lengths_example = streak.calculate_streak_lengths(list_checks_example, 86400)
    average_streak_length_example = statistics.ratio_streaks(list_streak_lengths_example, 31)
    assert abs(average_streak_length_example - (28/31)) < 0.0001