from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()
driver.get('http://info.classroomav.vt.edu/RoomSchedule.aspx')

#Checks all the correct boxes
full_schedule = driver.find_element_by_id("scheduleFull")
full_schedule.click()
show_events = driver.find_element_by_id("showEvents")
show_events.click()
show_past_events = driver.find_element_by_id("showPastEvents")
show_past_events.click()
show_GA_rooms = driver.find_element_by_id("showGARooms")
show_GA_rooms.click()

#Opens and selects building from dropdown
open_building_list = driver.find_element_by_id("PageBody_lstBuildings")
open_building_list.click()
select_building = Select(driver.find_element_by_id("PageBody_lstBuildings"))
build_list = select_building.all_selected_options
while build_list[0].text != "Wood Processing Lab":
	open_building_list.send_keys(Keys.DOWN)
	time.sleep(1)
	open_building_list.click()
	select_building = Select(driver.find_element_by_id("PageBody_lstBuildings"))
	build_list = select_building.all_selected_options
	print(build_list[0].text)
	room_list = driver.find_element_by_id("PageBody_lstRooms")
	select_room = Select(room_list)
	time.sleep(.4)
	selected_room = select_room.all_selected_options
	if(selected_room[0].text == "Select Room"):
		room_list.send_keys(Keys.DOWN)
		time.sleep(2)
		room_list.click()
		selected_room = select_room.all_selected_options
		time.sleep(.4)
		condition = True
		temp = select_room.all_selected_options
		while(condition == True):
			print("    " +selected_room[0].text)
			room_list.send_keys(Keys.DOWN)
			time.sleep(1)
			room_list.click()
			selected_room = select_room.all_selected_options
			if(temp == selected_room):
				condition = False
			temp = select_room.all_selected_options
	# for room in room_list:
	# 	print(build_list[0].text + ": " + room.text)


#Gets the list of rooms for a specific building
# select = Select(driver.find_element_by_id("PageBody_lstRooms"))
# room_list = select.all_selected_options
# for room in room_list:
# 	print(room.text)
#soup = BeautifulSoup(driver.page_source, "lxml")
#print(soup)