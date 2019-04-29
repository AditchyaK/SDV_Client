import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()

for i in range(100):
    kit.stepper2.onestep()
