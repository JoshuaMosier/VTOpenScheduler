from flask import Flask
from flask import request

app = Flask(__name__)

from flask import render_template

from scripts import event_dicts

@app.route('/')

@app.route('/index')
def index():
    schedules = event_dicts.get_nearby_schedules("McBryde Hall","100")
    total_dict = event_dicts.total_dict
    return render_template('index.html', schedules = schedules, total_dict=total_dict, result = None)

@app.route('/handle_data', methods=['POST'])
def handle_data():
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
    else:
    	result = None
    return render_template('index.html', building = building, rooms = rooms, total_dict = event_dicts.total_dict, days = event_dicts.get_day_list())

app.jinja_env.globals.update(get_sorted_times = event_dicts.get_sorted_times)
app.jinja_env.globals.update(get_string_format = event_dicts.get_string_format)
app.jinja_env.globals.update(get_list_format = event_dicts.get_list_format)

if __name__ == '__main__':
    app.run(debug=True)