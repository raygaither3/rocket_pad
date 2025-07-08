from flask import Blueprint, render_template, redirect, request, Response
import requests
import threading
import time
import csv
import os
import platform
from dotenv import load_dotenv
from pathlib import Path

from .flight_recorder import record_flight

# Explicitly load .env from project root
dotenv_path = Path(__file__).parent.parent / ".env"
print("DOTENV PATH =", dotenv_path)
print("EXISTS =", dotenv_path.exists())
load_dotenv(dotenv_path)

print("DEBUG ENV CHECK:", os.getenv("IS_PRODUCTION"))

IS_PRODUCTION = os.getenv("IS_PRODUCTION", "False") == "True"
print("IS_PRODUCTION =", IS_PRODUCTION)

gpio = None
if not IS_PRODUCTION and platform.system() != "Windows":
    from gpio_controller import GPIOController
    gpio = GPIOController()

# -- Config
bp = Blueprint("main", __name__)

PI_IP = os.getenv("PI_IP", "http://192.168.1.86:8080")
PI_API = os.getenv("PI_API", "http://192.168.1.86:8080")
PI_TEMP = os.getenv("PI_TEMP", "http://192.168.1.86:5050/temperature")

# -- System status
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

# -- Engine specs
data = {
    "A8-3": {"name": "A8-3", "avg_thrust": "2.5", "impulse": "2.5", "burn_time": "0.5", "weight_range": "50–100"},
    "B6-4": {"name": "B6-4", "avg_thrust": "4.3", "impulse": "5.0", "burn_time": "0.8", "weight_range": "100–150"},
    "C6-5": {"name": "C6-5", "avg_thrust": "6.0", "impulse": "10.0", "burn_time": "1.0", "weight_range": "150–200"},
    "D12-7": {"name": "D12-7", "avg_thrust": "10.0", "impulse": "20.0", "burn_time": "1.6", "weight_range": "200–300"}
}

# -- Helpers
def log_event(event):
    with open("launch_log.csv", "a", newline="") as f:
        csv.writer(f).writerow([time.strftime("%Y-%m-%d %H:%M:%S"), event])

def safe_gpio_call(func, *args, **kwargs):
    try:
        if gpio:
            func(*args, **kwargs)
    except Exception as e:
        print(f"GPIO call failed: {e}")

def launch_sequence():
    for i in range(5, 0, -1):
        status["countdown"] = i
        time.sleep(1)
        if status["aborted"]:
            log_event("Launch Aborted")
            return
    try:
        requests.get(f"{PI_API}/launch", timeout=5)
        log_event("Remote Launch Triggered")
    except Exception as e:
        log_event(f"Remote Launch FAILED: {e}")

# -- Routes safe everywhere
@bp.route("/")
def home():
    return render_template("landing.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/hangar")
def hangar():
    return render_template("hangar.html")

@bp.route("/hangar/mission-planning", methods=["GET", "POST"])
def mission_planning():
    altitude = None
    if request.method == "POST":
        weight = float(request.form.get("weight", 0))
        engine = request.form.get("engine")
        thrust = {"A": 200, "B": 400, "C": 800, "D": 1600}.get(engine, 0)
        altitude = int((thrust / weight) * 100)
    return render_template("hangar/mission_planning.html", altitude=altitude)

@bp.route("/hangar/engines", methods=["GET", "POST"])
def engines():
    engine_list = list(data.values())
    selected_engine = None
    if request.method == "POST":
        selected = request.form.get("engine")
        selected_engine = data.get(selected)
    return render_template("hangar/engines.html", engines=engine_list, selected_engine=selected_engine)

@bp.route("/hangar/physics")
def rocket_physics():
    return render_template("hangar/rocket_physics.html")

@bp.route("/hangar/parachutes")
def parachutes():
    return render_template("hangar/parachutes.html")

@bp.route("/hangar/environment")
def environment():
    return render_template("hangar/environment.html")

# -- Conditional routes for dashboard & hardware
if IS_PRODUCTION:
    @bp.route("/dashboard")
    def index():
        return render_template("coming_soon.html")

else:
    @bp.route("/dashboard")
    def index():
        stream_url = f"{PI_IP}/video_feed"

        try:
            res = requests.get(PI_TEMP, timeout=2)
            data = res.json()
            temp_c = data.get("temp_c")
            temp_f = data.get("temp_f")
        except Exception as e:
            print("Failed to fetch temp:", e)
            temp_c = temp_f = None

        return render_template("index.html", status=status, stream_url=stream_url, temp_c=temp_c, temp_f=temp_f)

    @bp.route("/toggle_safety")
    def toggle_safety():
        status["armed"] = not status["armed"]
        log_event("Safety Armed" if status["armed"] else "Safety Disarmed")

        try:
            requests.post(f"{PI_IP}/status-led", json={
                "armed": status["armed"],
                "launched": status["launched"]
            })
        except Exception as e:
            print("LED status update failed:", e)

        return redirect("/dashboard")

    @bp.route("/launch")
    def launch():
        if status["armed"] and not status["launched"]:
            status["aborted"] = False
            status["launched"] = True
            log_event("Launch Triggered")

            try:
                requests.post(f"{PI_IP}/status-led", json={
                    "armed": False,
                    "launched": True
                })
            except Exception as e:
                print("LED status update failed:", e)

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
        try:
            requests.get(f"{PI_API}/start_camera", timeout=5)
            status["camera_on"] = True
            log_event("Camera Started")
        except Exception as e:
            log_event(f"Camera start failed: {e}")
        return redirect("/dashboard")

    @bp.route("/stop_camera")
    def stop_camera_route():
        try:
            res = requests.get(f"{PI_API}/stop_camera", timeout=3)
            if res.ok:
                status["camera_on"] = False
                log_event("Remote camera stopped")
        except Exception as e:
            log_event(f"Failed to stop camera: {e}")
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

if gpio:
    import atexit
    atexit.register(lambda: gpio.cleanup())