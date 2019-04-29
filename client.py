import sys, socket, time
from adafruit_motorkit import MotorKit

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

#a very long fuction which just returns controller values
def setControlVar(data):
    return data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17]

#this function splits the incoming string which contains xbox controller input into
#an array of integers (for the buttons) and floating point numbers (for others)
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

#WIP: this function is responsible for toggling a button 
def buttonToggle(buttonVal, prevVal):
    if buttonVal:
        if (prevVal == 0):
            prevVal = 1
        else:
            prevVal = 0
        return prevVal, prevVal
    else:
        return prevVal, buttonVal

#this class contains all the control methods such as for the claw, motors and lights
class controlsClass:
    #this claw function is responsible for controlling the claw with two buttons
    def claw(self, button1, button2):
        if button1:
            kit.motor1.throttle = 1.0 #change sign according to polarity
        elif button2:
            kit.motor1.throttle = -1.0 #change sign according to polarity
        else:
            kit.motor1.throttle = 0
    #this function turns the lights on or off when (some button) is pressed
    def lights(self, button):
        if button: #set as a toggle when you fix it
            #lights on
        else:
            #lights off
    def 

"""
This is the actual start of the main loop which checks for data being
sent by the server and converting it to an array of values to use as controls
"""
#initializing controls class
controls = controlsClass()

#initalizing the MotorKit class
try:
    kit = MotorKit()
    print("Motor Class has been initialized")
except:
    print("Motor Class could not be initialized")

#creating a scoket and then setting it to resuse the port when shut down
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket has been created")

#initalizing host and port variables
port = 5558
host = '169.254.227.12'

#client socket connects to the server with static ip address
try: 
    s.connect((host, port))
    print("Socket successfully binded to ", host, " on port ", port)
except socket.error as msg:
    print("Socket failed to connect to host /n", msg)

#main loop for the program -> checks for data being sent by server in packets and
#then sending respective input to the cntroller class which operates motors
while True:
    data = s.recv(1024)
    data = data.decode('utf-8')
    #this disconnects the client (this device) from the server
    if (data == "KILL"):
        break
    #this is to set motors to stop when the controller is disconnected
    elif (data == "HOLD"):
        #stop all motors
        print("HOLD")
    data = splitData(data)
    A, B, X, Y, LH, RH, DU, DD, DL, DR, LB, RB, LX, LY, RX, RY, LT, RT = setControllerVar(data)
    controls.claw(A, B)
    """
    data[0], prevVal = buttonToggle(data[0], prevVal) fix this toggle
    print("")
    for i in range(len(data)):
        print(str(data[i]), end=" ")
    """

#cleaning up everything at the end
conn.close()
s.close()
print("\nYou have been disconnected from the server")
sys.exit()