import copy
import collections
from datetime import datetime

inputfile = open('textfiles/Rooms by Building.txt')
my_text = inputfile.readlines()
build_dict = {}
room = {}

#Revsered order so it generates a room dict first
for line in reversed(my_text):
	#Isolate out buildings
	if '    ' not in line:
		build_dict[line.strip()] = room
		room = {}
	else:
		room[line.strip()] = line.strip()


inputfile.close()

inputfile = open('textfiles/sorted_times.txt')
my_text = inputfile.readlines()
days = {'mon': [], 'tues': [], 'wed': [], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
currTime = {}

#This gets a dictionary for classes
total_dict = copy.deepcopy(build_dict)
for line in reversed(my_text):
	#Gets the current Building/Room Pair
	if '    ' not in line:
		currB = line.split(':')[0].strip()
		currR = line.split(':')[1].strip()
		total_dict[currB][currR] = currTime
		currTime = {}
		#print(buildings[currB][currR])
	elif 'Time' in line:
		currTime[line.split('                ')[1].strip()] = days
		days = {'mon': [], 'tues': [], 'wed': [], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
	elif 'Classes'  or 'Events' in line:
		for key in days:
			if key in line:
				if 'Classes' in line:
					class_info = []
					removed_day = line.split('                    ',1)[1].strip()
					sep_classes = removed_day.split('    ')
					for info in sep_classes:
						#Subject + Course number, CRN, Prof
						removed_subj = info.split("CRN: ")[0].strip()
						CRN = info.split("CRN: ")[1][:5].strip()
						prof = info.split("CRN: ")[1][5:].strip()
						class_info.append(removed_subj)
						class_info.append(CRN)
						class_info.append(prof)
					days[key] = class_info
				elif 'Events' in line:
					class_info = []
					removed_day = line.split('                    ',1)[1].strip().replace("&nbsp;","")
					date_range = removed_day.split('  ',1)[0].strip()
					details = removed_day.split('  ',1)[1].strip()
					purpose = details.split('  ',1)[0].strip()
					sub_details = details.split('  ',1)[1].strip()
					organizer = sub_details.split('N:')[1].strip()
					group = sub_details.split('N:',1)[0].strip().replace('D: ',"")
					class_info.append(date_range)
					class_info.append(purpose)
					class_info.append(group)
					class_info.append(organizer)
					days[key] = class_info

# #Print out the keys for the building
# for key in build_dict.items():
# 	print(key)

# #Print out the keys for classes/events
# for key in total_dict.items():
# 	print(key)

def get_build_codes():
	inputfile = open('textfiles/Building Names.txt')
	my_text = inputfile.readlines()
	build_codes = {}
	for line in my_text:
		split = line.split(' - ')
		key = split[0].strip()
		name = split[1].strip()
		build_codes[key] = name
	return build_codes

#Get a list of rooms for a given building name or building key
def get_room_list(building):
	build_codes = get_build_codes()
	if building in build_dict.keys():
		room_dict = build_dict[building]
	elif build_codes[building] in build_dict.keys():
		room_dict = build_dict[build_codes[building]]
	else:
		return None
	room_list = []
	for index,key in enumerate(collections.OrderedDict(sorted(room_dict.items()))):
		room_list.append(key)
	return room_list

#Testing get_room_list
#print(get_room_list("McBryde Hall"))

#Get a list of rooms +/- 5 from a given building/room combo
def get_nearby(building,room):
	room_list = get_room_list(building)
	index = room_list.index(room) if room in room_list else -1
	if index != -1:
		lower = index-5
		upper = index+6
		if lower  < 0:
			lower = 0
		if upper > len(room_list)-1:
			upper = len(room_list)-1
	else:
		return None
	return room_list[lower:upper]

#Testing get_nearby
#print(get_nearby("Cowgill Hall","300"))

#Get the schedule for a list of rooms
def get_schedules(building, rooms):
	class_schedules = []
	for room in rooms:
		class_schedules.append(total_dict[building][room])
	return class_schedules

# #Testing get_schedules
building_name = "TORG"
room_number = "1010"
# room_list = get_nearby(building_name,room_number)
# for index,schedule in enumerate(get_schedules(building_name,room_list)):
# 	print("Building: " + building_name + " Room: " + room_list[index])
# 	print(get_schedules(building_name,get_nearby(building_name,room_number))[index])
# 	print()

#Converts a time range string to datetime
def convert_to_datetime(time):
	times = time.split(' - ')
	start_in_time = datetime.strptime(times[0], "%I:%M %p")
	start_out_time = datetime.strftime(start_in_time, "%H:%M")
	end_in_time = datetime.strptime(times[1], "%I:%M %p")
	end_out_time = datetime.strftime(end_in_time, "%H:%M")
	return start_out_time + " - " + end_out_time


#Testing convert_to_datetime
#print(convert_to_datetime("7:00 AM - 10:59 PM"))


#Get the sorted order of times by dict keys
def get_sorted_times(building,room):
	if building in total_dict:
		class_sched = total_dict[building][room]
	elif build_codes[building] in total_dict:
		class_sched = total_dict[build_codes[building]][room]
	else:
		print("Incorrect Building or Building Code")
	combined_times = []
	time_dict = {}
	sorted_times = []
	#Converts the times for sorting
	for time in class_sched:
		time_dict[convert_to_datetime(time)] = time
	#Outputs sorted times in 24H
	# for key in collections.OrderedDict(sorted(time_dict.items())):
	# 	print(key)
	for key in collections.OrderedDict(sorted(time_dict.items())):
		sorted_times.append(time_dict[key])
	return sorted_times

# #Testing get_sorted_times
# print(get_sorted_times(building_name,room_number))

#Get all the schedules from nearby rooms
def get_nearby_schedules(building,selected_room):
	room_list = get_nearby(building,selected_room)
	schedules = []
	for room in room_list:
		schedules.append(get_sorted_times(building,room))
	return schedules

# #Testing get_nearby_schedules
# schedules = get_nearby_schedules(building_name,room_number)
# rooms_in_building = get_room_list(building_name)
# for index,schedule in enumerate(schedules):
# 	print("Building: " + building_name + " Room: " + rooms_in_building[index])
# 	print(schedule)
# 	print()

#Print out an individual schedule real nice like
def print_schedule(bldg,rm):
	if bldg in total_dict:
		building = bldg
	elif build_codes[bldg] in total_dict:
		building = build_codes[bldg]
	else:
		print("Incorrect Building or Building Code")
	week = ['mon','tues','wed','thurs','fri','sat','sun']
	times = get_sorted_times(building,room)
	print("Building: " + building + " Room: " + room)
	for time in times:
		print('\t' +time)
		for day in week:
			if total_dict[building][room][time][day]:
				print('\t\t' + day)
			for event in total_dict[building][room][time][day]:
				print('\t\t\t' + event)
		print()


#Tests print_schedule
#print_schedule(building_name,room_number)

# #Tests printing out the schedules of all nearby rooms
# room_list = get_nearby(building_name,room_number)
# for room in room_list:
# 	print_schedule(building_name,room)
# 	print()