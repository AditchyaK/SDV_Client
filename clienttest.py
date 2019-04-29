import sys, socket, time
from adafruit_motorkit import MotorKit

port = 5558
host = '169.254.227.12'
prevVal = 0
keys = ("AB", "BB", "XB", "YB", "LH", "RH", "DU", "DD", "DL", "DR", "LB", "RB", "LX", "LY", "RX", "RY", "LT", "RT", "END")

"""
AB = minirov motor backwards
BB = minirov motor forwards
XB = minirov winch backwards
YB = minirov winch forwards

LH = toggle lights
RH = 

DU = 
DD = 
DL = 
DR = 

LB = Toggle Claw open/close
RB = Toggle vertical motors up/down

LX = 
LY = Left motor forward/back
RX = 
RY = Right motor forward/back

LT = move claw
RT = move vertical motors

"""

def splitData(data):
    datatru = []
    datanu = data.split(keys[0])
    for i in range(len(keys)-1):
        i+= 1
        datanu = datanu[1].split(keys[i], 1)
        datatru.append(datanu[0])
    for i in range(len(datatru)):
        try:
            datatru[i] = int(datatru[i])
        except:
            datatru[i] = float(datatru[i])
    return datatru

def buttonToggle(buttonVal, prevVal):
    if buttonVal:
        if (prevVal == 0):
            prevVal = 1
        else:
            prevVal = 0
        return prevVal, prevVal
    else:
        return prevVal, buttonVal

class controlsClass:
    def claw(self, button1, button2):
        if button1:
            kit.motor1.throttle = 1.0 #change sign according to polarity
        elif button2:
            kit.motor1.throttle = -1.0 #change sign according to polarity
        else:
            kit.motor1.throttle = 0

"""
This is the actual start of the main loop which checks for data being
sent by the server and converting it to an array of values to use as controls
"""
#initializing controls class
controls = controlsClass()

try:
    kit = MotorKit()
    print("Motor Class has been initialized")
except:
    print("Motor Class could not be initialized")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket has been created")

try: 
    s.connect((host, port))
    print("Socket successfully binded to ", host, " on port ", port)
except socket.error as msg:
    print("Socket failed to connect to host /n", msg)

while True:
    data = s.recv(1024)
    data = data.decode('utf-8')
    if (data == "KILL"):
        break
    elif (data == "HOLD"):
        #stop all motors
        print("HOLD")
    data = splitData(data)
    controls.claw(data[0], data[1])
    """
    data[0], prevVal = buttonToggle(data[0], prevVal) fix this toggle
    print("")
    for i in range(len(data)):
        print(str(data[i]), end=" ")
    """

s.close()
print("\nYou have been disconnected from the server")
sys.exit()
