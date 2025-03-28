#!/usr/bin/python3
from flask import Flask, render_template, jsonify
import time
import random

app = Flask(__name__)

@app.route('/')
def index():
    # Renders the live dashboard (index.html)
    return render_template('index.html')

@app.route('/historic')
def historic():
    # Renders the historic data page (historic.html)
    return render_template('historic.html')

@app.route('/data')
def fake_data():
    """
    Returns multiple fake data points to simulate "live" data with history.
    This endpoint returns arrays for BPM, EAR, and timestamps so that the charts have multiple points.
    """
    num_points = 30  # number of data points to return
    current_time = time.time()
    # Create timestamps for the last 30 seconds (oldest first)
    timestamps = [time.strftime("%H:%M:%S", time.localtime(current_time - i)) for i in range(num_points)]
    timestamps.reverse()
    
    # Generate arrays for BPM and EAR data
    bpm = [round(random.uniform(60, 100), 2) for _ in range(num_points)]
    ear = [round(random.uniform(0.2, 0.4), 3) for _ in range(num_points)]
    
    # Fake model accuracy (could be a percentage)
    model_accuracy = round(random.uniform(0, 1), 2)
    
    # Fake LiDAR data remains a single reading
    lidar = {
        "right_distance": random.randint(100, 200),
        "left_distance": random.randint(100, 200),
        "too_close": random.choice([True, False]),
        "offsets": [[round(ang, 2), round(100 + ang * 20, 2)] for ang in [0.5, 1.0, 1.5]],
        "intensities": [random.randint(40, 80) for _ in range(3)]
    }
    
    alert = random.choice(["ALERT_ON", "ALERT_OFF"])
    
    return jsonify({
        "bpm": bpm,
        "ear": ear,
        "timestamps": timestamps,
        "model_accuracy": model_accuracy,
        "lidar": lidar,
        "alert": alert
    })

@app.route('/historic_data')
def historic_data():
    """
    Returns a list of multiple fake data points to simulate historic readings.
    """
    data_points = []
    for i in range(30):
        # Each point is i minutes in the past
        timestamp_str = time.strftime("%H:%M:%S", time.localtime(time.time() - i*60))
        data_points.append({
            "timestamp": timestamp_str,
            "bpm": round(random.uniform(60, 100), 2),
            "ear": round(random.uniform(0.2, 0.4), 3)
        })

    data_points.reverse()
    return jsonify(data_points)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
