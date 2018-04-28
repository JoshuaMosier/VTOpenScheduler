import re
from bs4 import BeautifulSoup

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
	ret = TAG_RE.sub(' ', text)
	ret.replace("&nbsp;", "")
	print(ret)
	return ret

# inputfile = open('events_example.html')
# my_text = inputfile.readlines()

# for line in my_text:
# 	if remove_tags(line).strip() is not "":
# 		print(remove_tags(line))

inputfile = open('export_events.txt')
my_text = inputfile.readlines()

sortedTimes = open('sorted_times.txt','w')

for line in my_text:
	if '<' not in line and line.strip() != "":
		sortedTimes.write(line)
	else:
		soup = BeautifulSoup(line, "lxml")
		classes = soup.find("span", {"id" : re.compile('fullClassSchedule.*')})
		events = soup.find("span", {"id" : re.compile('fullEventSchedule.*')})
		if classes:
			classDay = classes.get('id').replace('_classInfo_0','').replace('fullClassSchedule_','')
			#Prints the class day/time
			if 'classTime' in classDay:
				sortedTimes.write('\t' + classDay)
			else:
				sortedTimes.write('\t\t' + classDay)
			sortedTimes.write(remove_tags(line))

		if events:
			eventDay = events.get('id').replace('_eventInfo_0','').replace('fullEventSchedule_','')
			#Prints the event day/time
			if 'eventTime' in eventDay:
				sortedTimes.write('\t' + eventDay)
			else:
				sortedTimes.write('\t\t' + eventDay)
			sortedTimes.write(remove_tags(line))

sortedTimes.close();

