import time
import csv
import random

should_record = True  # Shared flag

def get_altitude():
    return round(100 + random.uniform(-5, 5), 2)

def get_speed():
    return round(20 + random.uniform(-3, 3), 2)

def record_flight():
    global should_record
    with open("flight_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Altitude (m)", "Speed (m/s)"])
        while should_record:
            timestamp = time.strftime("%H:%M:%S")
            alt = get_altitude()
            speed = get_speed()
            writer.writerow([timestamp, alt, speed])
            print(f"{timestamp} | Alt: {alt} m | Speed: {speed} m/s")
            time.sleep(1)

# This part is only for testing directly
if __name__ == "__main__":
    record_flight()