import sys
from subprocess import Popen


runtest = Popen("python " + "/home/pi/Desktop/SDV_Client/runtest.py", shell=True)
testrun = Popen("python " + "/home/pi/Desktop/SDV_Client/testrun.py", shell=True)
