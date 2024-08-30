from datetime import datetime
from datetime import timezone


# Choosing 1st January 2024 as starting point for counting since it is a Monday.
lower_bound_date = datetime(2024, 1, 1, 0, 0, 0)
# Finding the right timezone to determine the correct time of day. 
local_timezone = datetime.now(timezone.utc).astimezone().tzinfo


def time_interval_index(timestamp, period_length, timezone_variable = local_timezone, infimum_date = lower_bound_date):
    """Function which determines the index for every time interval (days respectively weeks) which includes a timestamp since the starting point (= lower_boundary_date)."""
    # Determining the time difference in seconds between the local time zone and the UTC. 
    timezone_shift = timezone_variable.utcoffset(None).seconds
    # Calculating the index for a time interval which includes a timestamp. 
    return int(timestamp + timezone_shift - infimum_date.timestamp()) // period_length


def time_interval_boundaries(timestamp, period_length, timezone_variable = local_timezone):
    """Function to determine the boundaries of time intervals which include a timestamp."""
    # Determining the time difference in seconds between the local time zone and the UTC. 
    timezone_shift = timezone_variable.utcoffset(None).seconds
    # Determining the difference between the timestamp and the greatest time interval boundary which is smaller than or equal to the timestamp. 
    # Equivalent with the time of the day or week in seconds. 
    time_of_day_or_week = (timestamp + timezone_shift) % period_length
    # Calculating the time interval boundaries. 
    return (timestamp - time_of_day_or_week, timestamp - time_of_day_or_week + period_length)


def calculate_streak_lengths(list_timestamps, interval_length):
    """Function which gives back a list of the lengths of all the streaks of a particular habit."""
    # Giving back an empty list for habits with no check-off. 
    if len(list_timestamps) == 0:
        return[]
    # Giving back the elements (= indices of timestamps) of the list of timestamps. 
    timestamps_indices_of_list = map(lambda n: time_interval_index(n, interval_length), list_timestamps)
    streak_length = 1
    # Defining the list of the lengths of all the streaks of a particular habit. 
    list_streak_lengths = []
    last_timestamp_index = next(timestamps_indices_of_list)
    for element_index in timestamps_indices_of_list:
        index_difference = element_index - last_timestamp_index
        # For the case if a habit is checked-off more than once in a time interval. 
        if index_difference == 0:
            continue
        # Determining the length of a streak. 
        elif index_difference == 1:
            streak_length += 1
            last_timestamp_index = element_index
        # If a streak ends, save the length in the list and set the streak length back to 1. 
        else:
            list_streak_lengths.append(streak_length)
            streak_length = 1
            last_timestamp_index = element_index
    # Adding the currently ongoing streak in the list. 
    list_streak_lengths.append(streak_length)
    return list_streak_lengths


def return_streak_lengths_and_dates(list_timestamps, interval_length):
    """Function which gives back a list of the lengths of all the streaks of a particular habit."""
    # Giving back an empty list for habits with no check-off. 
    if len(list_timestamps) == 0:
        return[]
    # Giving back the elements (= indices of timestamps) of the list of timestamps. 
    timestamps_indices_of_list = map(lambda n: time_interval_index(n, interval_length), list_timestamps)
    streak_length = 1
    # Defining the list of the lengths of all the streaks of a particular habit. 
    list_streak_lengths_and_dates = []
    last_timestamp_index = next(timestamps_indices_of_list)
    current_begin_timestamp = time_interval_boundaries(list_timestamps[0], interval_length)[0]
    for timestamp_index, element_index in enumerate(timestamps_indices_of_list, start = 1):
        index_difference = element_index - last_timestamp_index
        # For the case if a habit is checked-off more than once in a time interval. 
        if index_difference == 0:
            continue
        # Determining the length of a streak. 
        elif index_difference == 1:
            streak_length += 1
            last_timestamp_index = element_index
        # If a streak ends, save the length in the list and set the streak length back to 1. 
        else:
            end_timestamp = time_interval_boundaries(list_timestamps[timestamp_index - 1], interval_length)[1]
            list_streak_lengths_and_dates.append((streak_length, current_begin_timestamp, end_timestamp))
            current_begin_timestamp = time_interval_boundaries(list_timestamps[timestamp_index], interval_length)[0]
            streak_length = 1
            last_timestamp_index = element_index
    # Adding the currently ongoing streak in the list. 
    end_last_timestamp = time_interval_boundaries(list_timestamps[-1], interval_length)[1]
    list_streak_lengths_and_dates.append((streak_length, current_begin_timestamp, end_last_timestamp))
    return list_streak_lengths_and_dates