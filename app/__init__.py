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
    bldg = search.split(' ')[0]
    rm = search.split(' ')[1]
    result = event_dicts.get_nearby_schedules(bldg,rm)
    return render_template('index.html', result = result)

if __name__ == '__main__':
    app.run(debug=True)