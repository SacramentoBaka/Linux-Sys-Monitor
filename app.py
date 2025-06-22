from flask import Flask, render_template, jsonify
import json
from datetime import datetime
import pytz

app = Flask(__name__)

# Custom Jinja2 filter to convert ISO 8601 UTC to Africa/Johannesburg readable format
@app.template_filter('human_time')
def human_time_filter(value):
    try:
        # Parse UTC ISO timestamp from the log
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        sa_tz = pytz.timezone('Africa/Johannesburg')
        # Convert to SAST
        dt = dt.replace(tzinfo=pytz.utc).astimezone(sa_tz)
        return dt.strftime("%A, %d %B %Y %H:%M:%S")
    except Exception:
        return value

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metrics-table')
def metrics_table():
    try:
        with open('/var/log/linux_monitor/metrics.json') as f:
            lines = f.readlines()[-100:]
            data = [json.loads(line) for line in lines]
        return render_template('metrics_table.html', metrics=data)
    except Exception as e:
        return render_template('metrics_table.html', metrics=[], error=str(e))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/metrics')
def metrics():
    try:
        with open('/var/log/linux_monitor/metrics.json') as f:
            lines = f.readlines()[-100:]
            data = [json.loads(line) for line in lines]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

