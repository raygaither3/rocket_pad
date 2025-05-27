from flask import Flask, render_template, request, redirect, send_from_directory
from mission_launch.gpio_controller import GPIOController
import csv
import time
import threading
import os

app = Flask(__name__)
gpio = GPIOController(mock=True)  # Set to False when running on Raspberry Pi

status = {
    "armed": False,
    "countdown": None,
    "launched": False,
    "aborted": False,
    "camera_on": False,
    "altitude": 0,
    "speed": 0,
    "recording": False
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

def record_flight():
    import random
    with open("flight_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Altitude (m)", "Speed (m/s)"])
        for _ in range(15):
            timestamp = time.strftime("%H:%M:%S")
            alt = round(100 + random.uniform(-5, 5), 2)
            speed = round(20 + random.uniform(-3, 3), 2)
            status["altitude"] = alt
            status["speed"] = speed
            writer.writerow([timestamp, alt, speed])
            time.sleep(1)
    status["recording"] = False

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/dashboard")
def index():
    return render_template("index.html", status=status)

@app.route("/toggle_safety")
def toggle_safety():
    status["armed"] = not status["armed"]
    log_event("Safety Armed" if status["armed"] else "Safety Disarmed")
    return redirect("/dashboard")

@app.route("/launch")
def launch():
    if status["armed"] and not status["launched"]:
        status["aborted"] = False
        threading.Thread(target=launch_sequence).start()
    return redirect("/dashboard")

@app.route("/abort")
def abort():
    status["aborted"] = True
    status["countdown"] = None
    log_event("Launch Aborted")
    return redirect("/dashboard")

@app.route("/start_camera")
def start_camera():
    status["camera_on"] = True
    log_event("Camera Started")
    return redirect("/dashboard")

@app.route("/stop_camera")
def stop_camera():
    status["camera_on"] = False
    log_event("Camera Stopped")
    return redirect("/dashboard")

@app.route("/start_recorder")
def start_recorder():
    if not status["recording"]:
        status["recording"] = True
        log_event("Recorder Started")
        threading.Thread(target=record_flight).start()
    return redirect("/dashboard")

@app.route("/stop_recorder")
def stop_recorder():
    status["recording"] = False
    log_event("Recorder Stopped")
    return redirect("/dashboard")

if __name__ == "__main__":
    if not os.path.exists("launch_log.csv"):
        with open("launch_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Event"])
    app.run(debug=True)