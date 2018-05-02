from flask import Flask
from flask import request
from datetime import date, datetime, timedelta

app = Flask(__name__)

from flask import render_template

from python import event_dicts

@app.route('/')

@app.route('/index')
def index():
    schedules = event_dicts.get_nearby_schedules("McBryde Hall","100")
    total_dict = event_dicts.total_dict
    return render_template('index.html', schedules = schedules, total_dict=total_dict, result = None)

@app.route('/handle_data', methods=['POST'])
def handle_data():
	#TODO Move this method to event_dicts to check for existing building
    search = request.form['searchInput']
    split = search.split(' ')
    codes = event_dicts.get_build_codes()
    if len(split) == 2:
    	building = split[0]
    	room = split[1]
    	if building in codes:
    		building = codes[building]
    		rooms = event_dicts.get_nearby(building,room)
    	else:
    		result = None
    		rooms = None
    elif len(split) == 3:
    	building = ' '.join(split[:2])
    	room = split[2]
    	if building in event_dicts.total_dict and room in event_dicts.total_dict[building]:
    		rooms = event_dicts.get_nearby(building,room)
    	else:
    		result = None
    		rooms = None
    else:
    	building = None
    	rooms = None
    	result = None
    return render_template('index.html', building = building, rooms = rooms, total_dict = event_dicts.total_dict, days = event_dicts.get_day_list(), time_span = event_dicts
        .time_span())

app.jinja_env.globals.update(get_sorted_times = event_dicts.get_sorted_times)
app.jinja_env.globals.update(get_string_format = event_dicts.get_string_format)
app.jinja_env.globals.update(get_list_format = event_dicts.get_list_format)
app.jinja_env.globals.update(start_time = event_dicts.start_time)
app.jinja_env.globals.update(get_event_length = event_dicts.get_event_length)
app.jinja_env.globals.update(formatted_table_input = event_dicts.formatted_table_input)
app.jinja_env.globals.update(start_time_list = event_dicts.start_time_list)

if __name__ == '__main__':
    app.run(debug=True)