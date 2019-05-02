import sys, socket, time, Adafruit_PCA9685
from adafruit_motorkit import MotorKit

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
        i += 1
        datanu = datanu[1].split(keys[i], 1)
        datatru.append(datanu[0])
    for i in range(len(datatru)):
        try:
            datatru[i] = int(datatru[i])
        except:
            datatru[i] = float(datatru[i])
    return datatru


#this class contains all the control methods such as for the claw, motors and lights
class controlsClass:
    #P1 and P2 are forward and backward thrusters+
    def thruster200P1(self, axis, n, d):
        nu = n
        axis *= d
        nu += axis
        pwm.set_pwm(1, 1, int(nu))
    def thruster200P2(self, axis, n, d):
        nu = n
        axis *= d
        nu += axis
        pwm.set_pwm(2, 1, int(nu))

    #P3 to P6 are up and down thrusters
    def thruster100P3(self, axis, n, d):
        nu = n
        axis *= d
        nu += axis
        pwm.set_pwm(3, 1, int(nu))
    def thruster100P4(self, axis, n, d):
        nu = n
        axis *= d
        nu += axis
        pwm.set_pwm(4, 1, int(nu))
    def thruster100P5(self, axis, n, d):
        nu = n
        axis *= d
        nu += axis
        pwm.set_pwm(5, 1, int(nu)):
    def thruster100P6(self, axis, n, d):
        nu = n
        axis *= d
        nu += axis
        pwm.set_pwm(6, 1, int(nu))

    def camServoP7():
        #figure out servo controls

    def lightsP8():
        #figure out light controls
        
    #this claw function is responsible for controlling the claw with two buttons
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
#initialize variables for thruster control
n = 1260
d = 300

#initializing controls class
controls = controlsClass()

#initalizing the MotorKit class
try:
    kit = MotorKit()
    print("Motor Class has been initialized")
except:
    print("Motor Class could not be initialized")

#initializing PWM class
try:
    pwm = Adafruit_PCA9685.PCA9685()
except:
    print("Could not initialize PCA9685")
    sys.exit()

pwm.set_pwm(1, 1, int(n))

#creating a socket and then setting it to resuse the port when shut down
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
    print("")
    if (data == "KILL"):
        for i in range(6):
            i += 1
            pwm.set_pwm(i, 1, int(n))
            time.sleep(1)
            pwm.set_pwm(i, 0, int(0))
        break
    #this is to set motors to stop when the controller is disconnected
    elif (data == "HOLD"):
        for i in range(6):
            i += 1
            pwm.set_pwm(i, 1, int(n))
        print("HOLD")
        break
    try:
        data = splitData(data)
        for i in range(len(data)):
            print(str(data[i]), end=" ")
    except:
        print("No Data")

    controls.thrusterTest(data[15], n, d)
    #A, B, X, Y, LH, RH, DU, DD, DL, DR, LB, RB, LX, LY, RX, RY, LT, RT = setControllerVar(data)
    #controls.claw(A, B)
        
#cleaning up everything at the end
s.close()
print("\nYou have been disconnected from the server")
sys.exit()
