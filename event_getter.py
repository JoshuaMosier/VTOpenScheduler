from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

#Parse Rooms by Building into a 2d list
inputfile = open('Rooms by Building.txt')
my_text = inputfile.readlines()
buildings = []
rooms = []

#Get pretty html
def beautiful_soup(html):
	soup = BeautifulSoup(html,"lxml")
	spans = soup.findAll('span')
	return spans

#Get a list of the buildings
for line in my_text:
	if '    ' not in line:
		buildings.append(line.rstrip())


#Get the rooms for each building
count = 0
for line in reversed(my_text):
	if '    ' in line:
		rooms.append(line.strip())
	else:
		rooms.insert(0,line.rstrip())
		buildings[count] = rooms
		rooms = []
		count = count + 1

# #print list of buildings
# for building in reversed(buildings):
# 	print(building)
# 	print("\n")

# #print the list of buildings by room
# for building in reversed(buildings):
# 	for room in reversed(building[1:]):
# 		print(building[0] + ": " + room)

#Initialize Driver
driver = webdriver.Chrome()
driver.get('http://info.classroomav.vt.edu/RoomSchedule.aspx')

#Commands to check specific boxes on webpage
full_schedule = driver.find_element_by_id("scheduleFull")
full_schedule.click()
show_events = driver.find_element_by_id("showEvents")
show_events.click()
show_past_events = driver.find_element_by_id("showPastEvents")
show_past_events.click()
show_GA_rooms = driver.find_element_by_id("showGARooms")
show_GA_rooms.click()

#open export file
f = open('export_events.txt','w')

#Use selenium to get a specific building/room combo
for building in reversed(buildings):
	select_building = Select(driver.find_element_by_id("PageBody_lstBuildings"))
	select_building.select_by_visible_text(building[0])
	for room in reversed(building[1:]):
		select_room = Select(driver.find_element_by_id("PageBody_lstRooms"))
		time.sleep(.1)
		select_room.select_by_visible_text(room)
		time.sleep(1)
		html = driver.find_element_by_id('FullClassScheduleTable').get_attribute('innerHTML')
		pretty_html = beautiful_soup(html)
		f.write(building[0] + ": " + room)
		f.write(html)

#close export file
f.close()
