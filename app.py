from flask import Flask, Response, render_template, redirect
from gpio_controller import GPIOController
import csv
import time
import threading
import os
import cv2

app = Flask(__name__)
gpio = GPIOController(mock=True)  # Set to False when running on Raspberry Pi

status = {
    "armed": False,
    "countdown": None,
    "launched": False,
    "aborted": False
}

def log_event(event):
    with open("launch_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), event])

def launch_sequence():
    for i in range(5, 0, -1):
        status["countdown"] = i
        time.sleep(1)
        if status["aborted"]:
            log_event("Launch Aborted")
            return
    gpio.trigger_launch()
    status["countdown"] = 0
    status["launched"] = True
    log_event("Launch Executed")

@app.route("/")
def index():
    return render_template("index.html", status=status)

@app.route("/toggle_safety")
def toggle_safety():
    status["armed"] = not status["armed"]
    log_event("Safety Armed" if status["armed"] else "Safety Disarmed")
    return redirect("/")

@app.route("/launch")
def launch():
    if status["armed"] and not status["launched"]:
        status["aborted"] = False
        threading.Thread(target=launch_sequence).start()
    return redirect("/")

@app.route("/abort")
def abort():
    status["aborted"] = True
    status["countdown"] = None
    log_event("Launch Aborted")
    return redirect("/")

# Simulated video feed using webcam
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    if not os.path.exists("launch_log.csv"):
        with open("launch_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Event"])
    app.run(debug=True)


if __name__ == "__main__":
    with open("launch_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Event"])
    app.run(debug=True)
