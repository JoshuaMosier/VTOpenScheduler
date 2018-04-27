import copy

inputfile = open('Rooms by Building.txt')
my_text = inputfile.readlines()
buildings = {}
room = {}

#Revsered order so it generates a room dict first
for line in reversed(my_text):
	#Isolate out buildings
	if '    ' not in line:
		buildings[line.strip()] = room
		room = {}
	else:
		room[line.strip()] = line.strip()


inputfile.close()

inputfile = open('sorted_times.txt')
my_text = inputfile.readlines()
days = {'mon': [], 'tues': [], 'wed': [], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
currTime = {}

#This gets a dictionary for classes
class_dict = copy.deepcopy(buildings)
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
event_dict = copy.deepcopy(buildings)
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
				class_info = []
				removed_day = line.split('                    ',1)[1].strip()
				date_range = removed_day.split('  ',1)[0]
				details = removed_day.split('  ',1)[1]
				class_info.append(date_range)
				class_info.append(details)
				days[key] = class_info

# #Print out the keys for the building
# for key in buildings.items():
# 	print(key)

#Print out the keys for classes
for key in class_dict.items():
	print(key)

# #Print out the keys for events
# for key in event_dict.items():
# 	print(key)