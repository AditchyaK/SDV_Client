import sys, time, Adafruit_PCA9685

try:
    pwm = Adafruit_PCA9685.PCA9685()
except:
    print ("Could not initialize PCA9685")
    sys.exit()

pwm.set_pwm(1, 1, int(1260))
print("Initializing motors...")
time.sleep(7)
print("Motor Forward test!")
pwm.set_pwm(1, 1, int(1560))
time.sleep(5)
print("Motor Back test!")
pwm.set_pwm(1, 1, int(960))
time.sleep(5)
print("Motor at rest")
pwm.set_pwm(1, 1, int(1260))
time.sleep(2)
print("Shutting down")
pwm.set_pwm(1, 0, int(0))
sys.exit()

"""
import time
from adafruit_motorkit import MotorKit

kit = MotorKit(address = 0x60)

kit.motor1.throttle = 1.0
time.sleep(2)
kit.motor1.throttle = 0

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()

while True:
    for i in range(200):
        kit.stepper2.onestep(style=stepper.SINGLE)
"""
