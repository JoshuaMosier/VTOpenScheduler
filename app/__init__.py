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
    if len(split) == 2:
    	if split[0] in event_dicts.total_dict and split[1] in event_dicts.total_dict[bldg]:
    		result = event_dicts.get_nearby_schedules(split[0],split[1])
    	else:
    		result = None
    elif len(split) == 3:
    	bldg = ' '.join(split[:2])
    	rm = split[2]
    	if bldg in event_dicts.total_dict and rm in event_dicts.total_dict[bldg]:
    		result = event_dicts.get_nearby_schedules(bldg,rm)
    	else:
    		result = None
    else:
    	result = None
    return render_template('index.html', result = result)

if __name__ == '__main__':
    app.run(debug=True)