# Ray's Space Station ✨

**Launch dreams. Log missions. Learn together.**

Ray's Space Station is a fun, educational, and visually engaging rocket launch control center. Built using Python and Flask, this project is designed for real-time telemetry, video streaming, and rocket ignition control. Originally created for family fun and STEM learning, it is quickly evolving into a modular platform others can use and build upon.

---

## 📈 Features

- 🚀 Launch and abort control with countdown sequence
- 🌐 Sleek NASA-style dashboard UI with live data feed
- 📉 Real-time simulated telemetry: altitude & speed
- 🎥 Start/Stop live video stream toggle
- 🗂 Flight data logging and downloadable CSVs
- 🔌 GPIO mock + real hardware mode for Raspberry Pi
- 🏑 Designed for families, makers, and future rocket scientists

---

## 📦 Tech Stack

- Python 3.11
- Flask
- OpenCV (camera + frame handling)
- GPIO (with mock interface for dev)
- HTML/CSS with Orbitron font

---

## ⚙️ Setup & Run

1. Clone this repo
2. (Recommended) Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Visit `http://127.0.0.1:5000` in your browser

---

## 🕚 Roadmap

- [x] Launch button with countdown & safety toggle
- [x] Real-time simulated sensor readout
- [x] Video stream toggle and camera integration
- [x] Cool NASA-style UI with animated star background
- [ ] Flight history archive w/ playback
- [ ] Altitude and speed graph visualizations (live)
- [ ] Upload and showcase flight videos from others
- [ ] Download 3D rocket STL files for printing
- [ ] Mobile-friendly control panel
- [ ] Raspberry Pi GPIO relay control for live ignition
- [ ] Expandable community feature: share flights + results

---

## 🚗 Hardware Plans

- Raspberry Pi 3A+
- Relay module (for engine ignition)
- FPV camera (onboard video capture)
- Altitude sensor (BMP280 or similar)
- Battery + wireless hotspot for field launch

---

## 🌟 Inspiration

Built from scratch by a passionate maker and dad, Ray's Space Station is about family, fun, and fearless exploration.

---

## 👀 Live Demo
Coming soon!

---

## ✊ Contributions

Open to ideas, pull requests, and feedback!

---

## 👁️ License
MIT

---

## 🥳 Special Thanks

Thanks to my kids for inspiring this project ❤ and to the open-source community that makes ideas like this possible.

---
