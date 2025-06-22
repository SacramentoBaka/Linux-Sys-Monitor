from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    try:
        with open('/var/log/linux_monitor/metrics.json') as f:
            lines = f.readlines()[-100:]  # show last 100 entries
            data = [json.loads(line) for line in lines]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

