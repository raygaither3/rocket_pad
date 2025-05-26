# 🚀 Smart Rocket Pad (WIP)

This is an early-stage smart rocket launchpad controller built with Python and Flask. The app provides a web-based interface to **arm**, **launch**, and **abort** model rocket launches remotely — all controlled through a Raspberry Pi GPIO pin.

> ⚠️ **Disclaimer**: This project is currently in testing with mock GPIO output. It will be expanded to include real-time video feed, physical igniter triggering, and rocket-mounted camera modules.

---

## Features

- Web UI to control launch sequence
- Safety toggle (arming/disarming the pad)
- Countdown timer and status display
- Event logging to CSV
- GPIO abstraction with mock support (safe for development on non-Pi systems)

---

## Planned Features

- 🔴 Live video stream during countdown
- 🛰️ Rocket-mounted Pi Camera support
- 📶 Wi-Fi direct control via mobile device
- 🧠 Sensor feedback (accel/altimeter)
- 🔒 Launch verification / safety rules

---

## Setup

> Requires Python 3 and Flask. Safe to run on any machine for testing.

```bash
pip install flask
python rocket_pad/app.py
Then visit http://localhost:5000 to view the interface.

When running on a Raspberry Pi:

Set mock=False in gpio_controller.py to enable real GPIO output.

Connect GPIO pin 18 to a relay or MOSFET ignition circuit.

Directory Structure
bash
Copy
Edit
rocket_pad/
├── app.py                # Main Flask app and logic
├── gpio_controller.py   # GPIO abstraction (mock & real)
├── templates/
│   └── index.html       # Launch control interface
├── launch_log.csv       # Log of all launch events
Safety First
This project is built with safety in mind:

Launch cannot occur unless pad is armed

Manual abort available anytime during countdown

All events logged for traceability

Please ensure physical hardware is tested in a safe, open outdoor environment.

Author
Raymond Gaither III
🛠️ Self-taught developer | 🚀 Builder | 🔧 Raspberry Pi enthusiast
🌐 Portfolio

License
MIT License