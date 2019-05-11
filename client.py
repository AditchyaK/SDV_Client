import sys, socket, time, Adafruit_PCA9685, os, subprocess
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from adafruit_servokit import ServoKit

keys = ("AB", "BB", "XB", "YB", "LH", "RH", "DU", "DD", "DL", "DR", "LB", "RB", "LX", "LY", "RX", "RY", "LT", "RT", "END")

"""
Option 1

AB = minirov motor backwards
BB = minirov motor forwards
XB = minirov winch backwards
YB = minirov winch forwards

LH = 
RH = toggle lights

DU = 
DD = 
DL = 
DR = 

LB = Toggle Claw open/close
RB = Toggle vertical motors up/down

LX = 
LY = left motor forward/back
RX = 
RY = right motor forward/back

LT = move claw
RT = move vertical motors

Option 2

AB = minirov motor backwards
BB = minirov motor forwards
XB = minirov winch backwards
YB = minirov winch forwards

LH = 
RH = toggle lights

DU = 
DD = 
DL = 
DR = 

LB = claw open
RB = claw close

LX = yaw side motors
LY = up/dowm verical motors 
RX = roll vertical motors
RY = pitch vertical motors

LT = forward for side motors
RT = backward for side motors
"""

#a very long fuction which just returns controller values
def setControllerVar(data):
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
#--------------------------------------------------------------------------
#External thermometer address: 28-031897792ede

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-031897792ede/w1_slave'

def temp_raw():
    
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        lines = temp_raw()
        
    temp_output = lines[1].find('t=')
    
    if temp_output != -1:
        temp_string = lines [1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
#-----------------------------------------------------------------------------
#this class contains all the control methods such as for the claw, motors and lights
class controlsClass():
    #P1 and P2 are forward and backward thrusters

    """
    credit for the normalization of xbox controls to thruster control goes to Evan K.
    """
    
    def thruster100L(self, pwm, LT, RT, RX, n, d):
        nu = max(min(((d*(RT-LT))*(abs(RX)+1)+(d*RX)), d), -d)+n
        if nu != n:
            pwm.set_pwm(0, 1, int(nu))
        print(nu, end = " ")
    def thruster100R(self, pwm, LT, RT, RX, n, d):
        nu = max(min(((d*(RT-LT))*(abs(RX)+1)-(d*RX)), d), -d)+n
        if nu != n:
            pwm.set_pwm(1, 1, int(nu))
        print(nu, end = " ") 
        
    #P3 to P6 are up and down thrusters
    def thruster200FL(self, pwm, LX, LY, RY, n, d):
        nu = max(min(((d*LY)/(abs((LX-RY)/2)+1)-(d*((LX-RY)/2))), d), -d)+n
        if nu!= n:
                 pwm.set_pwm(2, 1, int(nu))
        print(nu, end = " ") 
    def thruster200FR(self, pwm, LX, LY, RY, axis, n, d):
        nu = max(min(((d*LY)/(abs((-LX-RY)/2)+1)-(d*((-LX-RY)/2))), d), -d)+n
        if nu!= n:
                 pwm.set_pwm(3, 1, int(nu))
        print(nu, end = " ") 
    def thruster200BL(self, pwm, LX, LY, RY, axis, n, d):
        nu = max(min(((d*LY)/(abs((LX+RY)/2)+1)-(d*((LX+RY)/2))), d), -d)+n
        if nu!= n:
                 pwm.set_pwm(4, 1, int(nu))
        print(nu, end = " ") 
    def thruster200BR(self, pwm, LX, LY, RY, axis, n, d):
        nu = max(min(((d*LY)/(abs((-LX+RY)/2)+1)-(d*((-LX+RY)/2))), d), -d)+n
        if nu!= n:
                 pwm.set_pwm(5, 1, int(nu))
        print(nu) 

    def stopAllMotors(self, n1, off):
        for i in range(6):
            pwm.set_pwm(i, 1, int(n1))
        if off:
            time.sleep(1)
            for i in range(6):
                pwm.set_pwm(i, 0, int(0))
            
    def claw (self, Mkit, button1, button2):
        if button1:
            Mkit.motor1.throttle = 1.0
        elif button2:
            Mkit.motor1.throttle = -1.0
        else:
            Mkit.motor1.throttle = 0
"""
This is the actual start of the main loop which checks for data being
sent by the server and converting it to an array of values to use as controls
"""
#----------------------------------------------------------------------------
#initialize variables for thruster control
n1 = 1260
d1 = 300

#initalizing the MotorKit class
try:
    Mkit = MotorKit()
    print("Motor Class has been initialized")
except:
    print("Motor Class could not be initialized")

time.sleep(1)

#initializing PWM class
try:
    pwm = Adafruit_PCA9685.PCA9685()
    print("PWM Class has been initialized")
except:
    print("Could not initialize PCA9685")
    sys.exit()

time.sleep(1)
for i in range(6):
    pwm.set_pwm(i, 1, int(n1))

#Servo Class initalizes here
try:
    Skit = ServoKit(channels=16)
    print("Servo Class has been initialized")
except:
    print("Servo Class could not be initialized")

time.sleep(1)

#initializing controls class
controls = controlsClass()

#creating a socket and then setting it to resuse the port when shut down
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket has been created")

#initalizing host and port variables
port = 5558
host = '169.254.227.12'

#--------------------------------------------------------------------
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
        controls.stopAllMotors(n1, 1)
        break
    
    #this is to set motors to stop when the controller is disconnected
    elif (data == "HOLD"):
        controls.stopAllMotors(n1, 0)
        break #change this for actual test

    #the data is split up into an array of integers and floating point values
    try:
        data = splitData(data)
        """
        for i in range(len(data)):
            print(str(data[i]), end=" ")
        """
    except:
        print("No Data")


    #button names are added for easy access
    A, B, X, Y, LH, RH, DU, DD, DL, DR, LB, RB, LX, LY, RX, RY, LT, RT = setControllerVar(data)

    #claw controls (RB out, LB in)
    controls.claw(Mkit, RB, LB)

    #yaw and forward/backward
    controls.thruster100L(pwm, LT, RT, RX, n1, d1)
    controls.thruster100R(pwm, LT, RT, RX, n1, d1)

    #pitching, rolling and vertical thrust
    controls.thruster200FL(pwm, LX, LY,RY, n1, d1)
    controls.thruster200FR(pwm, LX, LY,RY, n1, d1)
    controls.thruster200BL(pwm, LX, LY,RY, n1, d1)
    controls.thruster200BR(pwm, LX, LY,RY, n1, d1)
    
#cleaning up everything at the end
s.close()
print("\nYou have been disconnected from the server")
sys.exit()
