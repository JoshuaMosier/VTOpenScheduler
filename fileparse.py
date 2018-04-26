from datetime import datetime

with open("data.txt", 'r') as f:
    data = f.readlines()

valid_num_cols = [12,16,17]

classes = dict()

def add_class(location, days, time_range):
    if 'TBA' not in location:

        # Converts the string to a datetime object so it's more useful for us
        start, end = time_range
        dt_start = datetime.strptime(start, '%I:%M%p')
        dt_end = datetime.strptime(end, '%I:%M%p')
        dt_time_range = (dt_start, dt_end)

        # Goes until the first digit to find the room number
        for i, c in enumerate(location):
            if c.isdigit():
                building = location[:i].strip()
                room_num = location[i:].strip()
                break
            elif i == len(location)-1:
                # If the location doesn't contain a digit
                building = location.strip()
                room_num = ''

        if building not in classes:
            classes[building] = dict()

        if room_num not in classes[building]:
            # Create the day-by-day schedule
            init_rm_schedule = {'M': [], 'T': [], 'W': [], 'R': [], 'F': []}

            # Go thru each day in the "M W F" string and add the time range to
            # the rm_schedule for that day
            for day in days.split():
                if day in init_rm_schedule:
                    init_rm_schedule[day].append(dt_time_range)

            # Add the schedule to the room for that class
            classes[building][room_num] = init_rm_schedule

        else:
            # Same as in above loop
            for day in days.split(): #e.g. "M W F" -> ['M', 'W', 'F']
                if day in classes[building][room_num]:
                    classes[building][room_num][day].append(dt_time_range)

for line in data:
    cols = line.split('\t')
    if len(cols) not in valid_num_cols:
        continue

    if len(cols) == 12:
        [_, _, _, _, _, _, _, days, start, end, loc, _] = cols

    if len(cols) == 16:
        [_, _, _, _, _, _, _, _, _, _, _, _, days, start, end, loc] = cols

    if len(cols) == 17:
        [_, _, _, _, _, _, _, days, start, end, loc, _, _, days2, start2,
        end2, loc2] = cols
        add_class(loc2, days2, (start2, end2))

    add_class(loc, days, (start,end))

import pickle
with open('timetable.pkl', 'wb') as f:
    pickle.dump(classes, f)
