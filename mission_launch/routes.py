from flask import Blueprint, render_template, redirect
from .gpio_controller import GPIOController
from .flight_recorder import record_flight
from flask import Response
from .camera import start_camera, stop_camera, generate_frames
import csv
import time
import threading


bp = Blueprint("main", __name__)
gpio = GPIOController(mock=True)

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

@bp.route("/")
def home():
    return render_template("landing.html")

@bp.route("/dashboard")
def index():
    return render_template("index.html", status=status)

@bp.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@bp.route("/toggle_safety")
def toggle_safety():
    status["armed"] = not status["armed"]
    log_event("Safety Armed" if status["armed"] else "Safety Disarmed")
    return redirect("/dashboard")

@bp.route("/launch")
def launch():
    if status["armed"] and not status["launched"]:
        status["aborted"] = False
        threading.Thread(target=launch_sequence).start()
    return redirect("/dashboard")

@bp.route("/abort")
def abort():
    status["aborted"] = True
    status["countdown"] = None
    log_event("Launch Aborted")
    return redirect("/dashboard")

@bp.route("/start_camera")
def start_camera_route():
    status["camera_on"] = True
    log_event("Camera Started")
    start_camera()
    return redirect("/dashboard")

@bp.route("/stop_camera")
def stop_camera_route():
    status["camera_on"] = False
    log_event("Camera Stopped")
    stop_camera()
    return redirect("/dashboard")

@bp.route("/start_recorder")
def start_recorder():
    if not status["recording"]:
        status["recording"] = True
        log_event("Recorder Started")
        threading.Thread(target=record_flight).start()
    return redirect("/dashboard")

@bp.route("/stop_recorder")
def stop_recorder():
    status["recording"] = False
    log_event("Recorder Stopped")
    return redirect("/dashboard")