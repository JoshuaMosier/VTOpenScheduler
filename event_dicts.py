
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

for line in reversed(my_text):
	#Gets the current Building/Room Pair
	if '    ' not in line:
		currB = line.split(':')[0].strip()
		currR = line.split(':')[1].strip()
		buildings[currB][currR] = currTime
		currTime = {}
		#print(buildings[currB][currR])
	elif 'Time' in line:
		currTime[line.split('                ')[1].strip()] = days
		days = {'mon': [], 'tues': [], 'wed': [], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
	elif 'Classes' in line:
		for key in days:
			if key in line:
				class_info = []
				removed_day = line.split('                    ',1)[1].strip()
				#Subject + Course number
				removed_subj = removed_day.split("CRN: ")[0]
				class_info.append(removed_subj)
				#CRN
				CRN = removed_day.split("CRN: ")[1][:5]
				class_info.append(CRN)
				#Professor
				prof = removed_day.split("CRN: ")[1][5:]
				class_info.append(prof)
				days[key] = class_info

#Print out the keys for the building
for key in buildings.items():
	print(key)
