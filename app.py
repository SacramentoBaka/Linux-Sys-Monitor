from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=5000, debug=True)

