import copy
import collections

inputfile = open('Rooms by Building.txt')
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

inputfile = open('sorted_times.txt')
my_text = inputfile.readlines()
days = {'mon': [], 'tues': [], 'wed': [], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
currTime = {}

#This gets a dictionary for classes
class_dict = copy.deepcopy(build_dict)
for line in reversed(my_text):
	#Gets the current Building/Room Pair
	if '    ' not in line:
		currB = line.split(':')[0].strip()
		currR = line.split(':')[1].strip()
		class_dict[currB][currR] = currTime
		currTime = {}
		#print(buildings[currB][currR])
	elif 'classTime' in line:
		currTime[line.split('                ')[1].strip()] = days
		days = {'mon': [], 'tues': [], 'wed': [], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
	elif 'Classes' in line:
		for key in days:
			if key in line:
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

#reset stuff in case its breaking
inputfile.close()

inputfile = open('sorted_times.txt')
my_text = inputfile.readlines()
days = {'mon': [], 'tues': [], 'wed': [], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
currTime = {}

#This gets a dictionary for events
event_dict = copy.deepcopy(build_dict)
for line in reversed(my_text):
	#Gets the current Building/Room Pair
	if '    ' not in line:
		currB = line.split(':')[0].strip()
		currR = line.split(':')[1].strip()
		event_dict[currB][currR] = currTime
		currTime = {}
		#print(buildings[currB][currR])
	elif 'eventTime' in line:
		currTime[line.split('                ')[1].strip()] = days
		days = {'mon': [], 'tues': [], 'wed': [], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
	elif 'Events_' in line:
		for key in days:
			if key in line:
				#2/15/18 - 4/26/18  Club Meetings  D: Young Americans for Liberty N: Andrew Letzkus aletzkus@vt.edu (571) 292 &nbsp;
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
				#print(class_info)
				days[key] = class_info

# #Print out the keys for the building
# for key in build_dict.items():
# 	print(key)

# #Print out the keys for classes
# for key in class_dict.items():
# 	print(key)

# #Print out the keys for events
# for key in event_dict.items():
# 	print(key)

#Create Dictionary of Building codes --> Buidlings
inputfile = open('Building Names.txt')
my_text = inputfile.readlines()
build_codes = {}

for line in my_text:
	split = line.split(' - ')
	key = split[0].strip()
	name = split[1].strip()
	build_codes[key] = name


#Get a list of rooms for a given building name or building key
def get_room_list(building):
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
	return room_list[lower:upper]

#Testing get_nearby
#print(get_nearby("Cowgill Hall","300"))

#Get the schedule for a list of rooms
def get_schedules(building, rooms):
	class_schedules = []
	for room in rooms:
		class_schedules.append(class_dict[building][room])
	return class_schedules

#Testing get_schedules
building_name = "Cowgill Hall"
room_number = "300"
room_list = get_nearby(building_name,room_number)
for index,schedule in enumerate(get_schedules(building_name,room_list)):
	print("Building: " + building_name + " Room: " + room_list[index])
	print(get_schedules(building_name,get_nearby(building_name,room_number))[index])
	print()

#Nice output for a specific schedule
