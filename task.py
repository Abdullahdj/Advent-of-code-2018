#!/usr/bin/python
"""
Decomposition:
1)Read data from txt and convert to readable easy to manipulate data (list/array) done for me
2)Sort the data items by date
3)Collect sleep and wake times for each guard (most likely in a dictionary of lists)
"""


# Throughout i try to use the variable naming convention that i learnt of dr Pawson (use verbose names)
# Throughout i used example.txt and the data set from advent of code online to test my code
# I'm going to assume that all times that are relevant are between 00:00 and 00:59
# Also assuming that guards who start before or after 00:00 are awake at 00:00 upto the time they start

# sort by date all records (we know that all inputs are in the same format so this should be ez)
def sort_by_date(records):
    new_record = []
    # give the logs numerical values for sorting while keeping original record intact
    for log in records:  # logs look like: '[1518-11-01 00:00] Guard #10 begins shift'
        new_record.append(log + log[6] + log[7] + log[9] + log[10] + log[12] + log[13] + log[15] + log[
            16])  # num value is 8 char long
    # now use a simple insertion sort (edit of old code I have)
    for j in range(1, len(new_record)):
        newitem = new_record[j][-8:]
        i = j - 1
        while (i >= 0) and int(new_record[i][-8:]) > int(newitem):
            x = new_record[i + 1]
            new_record[i + 1] = new_record[i]
            new_record[i] = x
            i = i - 1
    return new_record


# Could definitely be made more readable and more efficient o(n^2) time complexity

# Create dictionary of lists for all sleep/wake times
def get_times(ordered_input):
    guard_times = {}
    for count in range(0, len(ordered_input)):
        if "#" in ordered_input[count]:
            index = ordered_input[count].index("#")
            current_guard_id = ""
            while ordered_input[count][index] == "#" or ordered_input[count][index].isdigit():
                if ordered_input[count][index] != "#":
                    current_guard_id += ordered_input[count][index]
                index += 1
            if current_guard_id not in guard_times:
                if int(ordered_input[count][-4:]) < 60:
                    guard_times[current_guard_id] = [ordered_input[count][-4:]]
                else:
                    guard_times[current_guard_id] = ["0000"]
        else:
            if int(ordered_input[count][-4:]) < 60:
                guard_times[current_guard_id].append(ordered_input[count][-4:])
            else:
                guard_times[current_guard_id].append("0000")
    return guard_times


# create a new dictionary that only has the minutes in which the guard slept making counting easy
def get_sleep_times(guard_times):
    guard_sleep_times = {}
    for guard in guard_times:
        guard_sleep_times[guard] = []
        count = 1
        for index in range(0, len(guard_times[guard])):
            try:
                if int(guard_times[guard][index]) < int(guard_times[guard][index + 1]) and (count % 2) == 0:
                    for x in range(int(guard_times[guard][index]), int(guard_times[guard][index + 1])):
                        guard_sleep_times[guard].append(x)
                elif (count % 2) == 0:
                    for x in range(int(guard_times[guard][index]), 60):
                        guard_sleep_times[guard].append(x)
            except IndexError:
                if (count % 2) == 0:
                    for x in range(int(guard_times[guard][index]), 60):
                        guard_sleep_times[guard].append(x)
            count += 1
    return guard_sleep_times


# everything combined for task 1
def task1(ordered_input):
    guard_times = get_times(ordered_input)
    guard_sleep_times = get_sleep_times(guard_times)
    sleepiest_guard = ["", 0]
    for guard in guard_sleep_times:
        if len(guard_sleep_times[guard]) > sleepiest_guard[1]:
            sleepiest_guard[0] = guard
            sleepiest_guard[1] = len(guard_sleep_times[guard])
    most_freq_time = [0, 0]
    for time in guard_sleep_times[sleepiest_guard[0]]:
        occurences = (guard_sleep_times[sleepiest_guard[0]]).count(time)
        if occurences > most_freq_time[0]:
            most_freq_time[0] = occurences
            most_freq_time[1] = time
    return int(most_freq_time[1]) * int(sleepiest_guard[0])


def get_freq_sleep_times(guard_sleep_times):
    freq_sleep_times = {}
    for guard in guard_sleep_times:
        most_freq_time = [0, 0]
        for time in guard_sleep_times[guard]:
            occurences = guard_sleep_times[guard].count(time)
            if occurences > most_freq_time[0]:
                most_freq_time[0] = occurences
                most_freq_time[1] = time
        freq_sleep_times[guard] = most_freq_time
    return freq_sleep_times


# copy paste of task one only with slight modifications
def task2(ordered_input):
    guard_times = get_times(ordered_input)
    guard_sleep_times = get_sleep_times(guard_times)
    freq_sleep_times = get_freq_sleep_times(guard_sleep_times)
    consistent_guard = ["no one", 0]
    for guard in freq_sleep_times:
        if freq_sleep_times[guard][0] > consistent_guard[1]:
            consistent_guard[0] = guard
            consistent_guard[1] = freq_sleep_times[guard][0]
    return int(consistent_guard[0]) * (freq_sleep_times[consistent_guard[0]][1])


# reads the file and makes each line separate in a list for me
def get_input(filename):
    with open(filename) as file:
        return [line.rstrip() for line in file]


records = sort_by_date(get_input('adventofcodedata.txt'))
print("Answer Task 1: ", task1(records.copy()))  # This code works for advent of code challenge
print("Answer Task 2: ", task2(records.copy()))  # This code also works
