class GPIOController:
    def __init__(self, mock=True):
        self.mock = mock
        if not mock:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            self.LAUNCH_PIN = 18
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.LAUNCH_PIN, GPIO.OUT)

    def trigger_launch(self):
        if self.mock:
            print("🚀 MOCK LAUNCH TRIGGERED")
        else:
            print("🚀 REAL LAUNCH TRIGGERED")
            self.GPIO.output(self.LAUNCH_PIN, self.GPIO.HIGH)
            time.sleep(1)
            self.GPIO.output(self.LAUNCH_PIN, self.GPIO.LOW)

    def cleanup(self):
        if not self.mock:
            self.GPIO.cleanup()