#!/usr/bin/env python3
# Import needed robot output and inputs
from ev3dev2.motor import LargeMotor, MoveTank, MediumMotor, SpeedPercent
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_C, OUTPUT_B
from ev3dev2.sensor.lego import GyroSensor, InfraredSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from multiprocessing import pool
from ev3dev2.sound import Sound
spkr = Sound()
# Initiate motors
bothmotors = MoveTank(OUTPUT_A, OUTPUT_D)
motorA = LargeMotor(OUTPUT_A)
motorD = LargeMotor(OUTPUT_D)
motorB = MediumMotor(OUTPUT_B)
motorB.on_for_rotations(-70,0.1)
#motorB = MediumMotor(OUTPUT_B)
# Initiate sensors
gyro = GyroSensor(INPUT_1)
bothmotors.gyro = GyroSensor(INPUT_1)
gyro.reset()
gyro.calibrate()
gyro.calibrate()

#infrared = InfraredSensor(INPUT_2)
colorSensor = ColorSensor(INPUT_4)

# Constants needed for precise movement & turning
circumferenceOfTire = 6.775 #inches move forward in one rotation
rotationOfBMotor = 1.25
baseAngle = gyro.circle_angle()
speed = 20

#try get variables for more precise turning
initialAngle = gyro.circle_angle() #also initializes to 90 after reseting/calibrating
direction1 = 90
direction2 = 0 
direction3 = 270
direction4 = 180
print("The initial angle is {0} degrees.".format(initialAngle))

#variable determing movement
direction = 1
distancex = 0
distancey = 0
case = 0
fulfill = 0
#for break 
flag = True

box = ["", 1,1,1,1]
box[0] = str(input("Which Shelve are we going to : "))
box[1] = int(input("Which unit of {0} are we going to (1,2): ".format(box[0])))
box[2] = int(input("What is the box number: "))
box[3] = int(input("Which barcode type is expected: "))
fulfillmentcenter = int(input("Which fulfillment center to drop off? (c=3,d=4,b=2) : "))

def correct():
    global direction,direction1,direction2,direction3, direction4
    currentangle = gyro.circle_angle()
    print("The current angle is {0}:".format(currentangle))
    morecorrect = 0
    if direction == 1:
        if currentangle < direction1:
            morecorrect = currentangle-direction1
            bothmotors.turn_degrees(speed=SpeedPercent(3), target_angle=morecorrect)
        else:
            morecorrect = direction1-currentangle
            bothmotors.turn_degrees(speed=SpeedPercent(3), target_angle=-morecorrect)    
    elif direction == 2:
        if currentangle < 300:
            morecorrect = currentangle
            bothmotors.turn_degrees(speed=SpeedPercent(3), target_angle=morecorrect)
        else:
            morecorrect = (360-currentangle)*-1
            bothmotors.turn_degrees(speed=SpeedPercent(3), target_angle=morecorrect)
    elif direction == 3:
        if currentangle < direction3:
            morecorrect = currentangle-direction3
            bothmotors.turn_degrees(speed=SpeedPercent(3), target_angle=morecorrect)
        else:
            morecorrect = direction3-currentangle
            bothmotors.turn_degrees(speed=SpeedPercent(3), target_angle=-morecorrect)
    elif direction == 4:
        if currentangle < direction4:
            morecorrect = currentangle-direction4
            bothmotors.turn_degrees(speed=SpeedPercent(3), target_angle=morecorrect)
        else:
            morecorrect = direction4-currentangle
            bothmotors.turn_degrees(speed=SpeedPercent(3), target_angle=-morecorrect)
    print("The direction is {0}".format(direction))
    print("Corrected by {0} degrees".format(morecorrect))
    print("Corrected to {0} degrees".format(gyro.circle_angle()))

def MoveForward(Ninches):
    rotationsneeded = Ninches / circumferenceOfTire
    bothmotors.on_for_rotations(-speed,-speed,rotationsneeded/3)
    correct()
    bothmotors.on_for_rotations(-speed,-speed,rotationsneeded/3)
    correct()
    bothmotors.on_for_rotations(-speed,-speed,rotationsneeded/3)
    correct()
    global distancex,distancey,direction
    if direction == 1:
        distancey += Ninches
    elif direction == 2:
        distancex += Ninches
    elif direction ==3:
        distancey -= Ninches
    elif direction == 4:
        distancex -= Ninches
    #print("After moving {0} inches, in direction {1},  the distance of x is {2}".format(Ninches,direction,distancex))
    #print("After moving {0} inches, in direction {1},  the distance of y is {2}".format(Ninches,direction,distancey))
    #print("The current angle is {0}".format(gyro.circle_angle()))


def TurnClockwise(degrees):
    global direction1,direction2,direction3,direction4
    global direction
    bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=degrees, sleep_time=0.01,brake=True)
    if degrees == 90:
        if direction==1:
            direction = 2
        elif direction ==2:
            direction = 3
        elif direction ==3:
            direction = 4
        elif direction ==4:
            direction = 1
    elif degrees == -90:
        if direction==1:
            direction = 4
        elif direction ==2:
            direction = 1
        elif direction ==3:
            direction = 2
        elif direction == 4:
            direction = 3
    elif degrees == 180:
        if direction==1:
            direction = 3
        elif direction ==2:
            direction = 4
        elif direction ==3:
            direction = 1
        elif direction == 4:
            direction = 2
    correct()

# Coordinate system for warehouse
# Aisles y-coordinate
Aisles = {"Aisle1" : 12, "Aisle2" : 36, "Aisle3" : 60, "Aisle4" : 84, "Aisle5" : 108}
# Corridor x-coordinate
Corridors = {"Corridor1" : 0, "Corridor2" : 48, "Corridor3" : 96}
#fulfill location y 
Fulfillsy = {"C" : 114, "D":114, "B" :0}

def MovementToBox(Box):
    #Movement is [move1,turnDeg1, CC OR CL, move2, turnDeg2. CC or CL...]
    Shelve = Box[0]
    ShelveNumber = int(Box[1])
    Boxnumber = int(Box[2])
    if Shelve == "A": #and ShelveNumber == 1 and Boxnumber < 7:
        if ShelveNumber == 1 and Boxnumber < 7:
            MoveForward(Aisles["Aisle1"])
            TurnClockwise(90)
            MoveForward(3+Boxnumber*6) 
        elif ShelveNumber == 1 and Boxnumber >= 7:
            MoveForward(Aisles["Aisle2"])
            TurnClockwise(90)
            MoveForward(3+(Boxnumber-6)*6)
        elif ShelveNumber == 2 and Boxnumber < 7:
            MoveForward(Aisles["Aisle2"])
            TurnClockwise(90)
            MoveForward(3+Boxnumber*6)
        elif ShelveNumber == 2 and Boxnumber >= 7:
            MoveForward(Aisles["Aisle3"])
            TurnClockwise(90)
            MoveForward(3+(Boxnumber-6)*6)
    elif Shelve == "B":
        if ShelveNumber == 1 and Boxnumber < 7:
            MoveForward(Aisles["Aisle1"])
            TurnClockwise(90)
            MoveForward(3+Corridors["Corridor2"])
            MoveForward(3+Boxnumber*6) 
        elif ShelveNumber == 1 and Boxnumber >= 7:
            MoveForward(Aisles["Aisle2"])
            TurnClockwise(90)
            MoveForward(3+Corridors["Corridor2"])
            MoveForward(3+(Boxnumber-6)*6)
        elif ShelveNumber == 2 and Boxnumber < 7:
            MoveForward(Aisles["Aisle2"])
            TurnClockwise(90)
            MoveForward(3+Corridors["Corridor2"])
            MoveForward(3+Boxnumber*6)
        elif ShelveNumber == 2 and Boxnumber >= 7:
            MoveForward(Aisles["Aisle3"])
            TurnClockwise(90)
            MoveForward(3+Corridors["Corridor2"])
            MoveForward(3+(Boxnumber-6)*6)
    elif Shelve == "C":
        if ShelveNumber == 1 and Boxnumber < 7:
            MoveForward(Aisles["Aisle3"])
            TurnClockwise(90)
            MoveForward(3+Boxnumber*6) 
        elif ShelveNumber == 1 and Boxnumber >= 7:
            MoveForward(Aisles["Aisle4"])
            TurnClockwise(90)
            MoveForward(3+(Boxnumber-6)*6)
        elif ShelveNumber == 2 and Boxnumber < 7:
            MoveForward(Aisles["Aisle4"])
            TurnClockwise(90)
            MoveForward(3+Boxnumber*6)
        elif ShelveNumber == 2 and Boxnumber >= 7:
            MoveForward(Aisles["Aisle5"])
            TurnClockwise(90)
            MoveForward(3+(Boxnumber-6)*6)
    elif Shelve == "D":
        if ShelveNumber == 1 and Boxnumber < 7:
            MoveForward(Aisles["Aisle3"])
            TurnClockwise(90)
            MoveForward(3+Corridors["Corridor2"])
            MoveForward(3+Boxnumber*6) 
        elif ShelveNumber == 1 and Boxnumber >= 7:
            MoveForward(Aisles["Aisle4"])
            TurnClockwise(90)
            MoveForward(3+Corridors["Corridor2"])
            MoveForward(3+(Boxnumber-6)*6)
        elif ShelveNumber == 2 and Boxnumber < 7:
            MoveForward(Aisles["Aisle4"])
            TurnClockwise(90)
            MoveForward(3+Corridors["Corridor2"])
            MoveForward(3+Boxnumber*6)
        elif ShelveNumber == 2 and Boxnumber >= 7:
            MoveForward(Aisles["Aisle5"])
            TurnClockwise(90)
            MoveForward(3+Corridors["Corridor2"])
            MoveForward(3+(Boxnumber-6)*6)
def MoveToHome(fulfill):
    if fulfill == 3:
        TurnClockwise(180)
        MoveForward(Fulfillsy["C"])
    elif fulfill == 4:
        TurnClockwise(180)
        MoveForward(Fulfillsy["C"] - 6)
        TurnClockwise(90)
        MoveForward(90)
        TurnClockwise(-90)
        MoveForward(6)
    else:
        TurnClockwise(180)
        MoveForward(6)
        TurnClockwise(-90)
        MoveForward(90)
        TurnClockwise(-90)
        MoveForward(8)
def MoveToFulfill(fulfill):
    if fulfill == 3:
        TurnClockwise(180)
        MoveForward(distancex)
        TurnClockwise(90)
        MoveForward(Fulfillsy["C"] - distancey)
    elif fulfill == 4:
        MoveForward(102-distancex)
        TurnClockwise(-90)
        MoveForward(Fulfillsy["C"] - distancey)
    elif fulfill == 2:
        MoveForward(102-distancex)
        TurnClockwise(90)
        MoveForward(distancey)      
def averageRGB(vals):
    total = vals[0] + vals[1] + vals[2]
    return total / 3
def determineType(box,barcode):
    matchBarcode = []
    Type1 = [1,1,1,0]
    Type2 = [1,0,1,0]
    Type3 = [1,1,0,0]
    Type4 = [0,1,1,0]
    if box[3] == 1:
        matchBarcode = Type1
    elif box[3] == 2:
        matchBarcode = Type2
    elif box[3] == 3:
        matchBarcode = Type3
    else:
        matchBarcode = Type4
    global flag
    if barcode == matchBarcode:
        flag = False
        print("The barcode matches type {0}.".format(box[3]))
        spkr.speak("The barcode mtaches type {0}".format(box[3]))
    else:
        if barcode== Type1:
            print("The incorrect barcode type is type 1.\n")
            spkr.speak("The incorrect barcode matches type 1")
        elif barcode == Type2:
            print("The incorrect barcode type is type 2.\n")
            spkr.speak("The incorrect barcode matches type 2")
        elif barcode == Type3:
            print("The incorrect barcode type is type 3.\n")
            spkr.speak("The incorrect barcode matches type 3")
        else:
            print("The incorrect barcode type is type 4.\n")
            spkr.speak("The incorrect barcode matches type 4")
    print("The location is {0}".format(box[:3]))
    spkr.speak("The location is {0}".format(box[:3]))


def ScanBarcode(box):
    colors= []
    rotationsneeded = 0.24
    if box[2] < 7:
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=45, sleep_time=0.01,brake=True)
        bothmotors.on_for_rotations(10,10,rotationsneeded)
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=-45, sleep_time=0.01,brake=True)
        print(averageRGB(colorSensor.rgb))
        print(colorSensor.reflected_light_intensity)
        while ((averageRGB(colorSensor.rgb) > 1 and averageRGB(colorSensor.rgb) < 5) or (averageRGB(colorSensor.rgb) < 80 and averageRGB(colorSensor.rgb) > 5)):
            print(averageRGB(colorSensor.rgb))
            print(colorSensor.reflected_light_intensity)
            bothmotors.on_for_rotations(10,10,0.01)
        if averageRGB(colorSensor.rgb) > 80:
                colors.append(1)
        else:
                colors.append(0)
        for i in range(3):
            bothmotors.on_for_rotations(10,10,0.075)
            if averageRGB(colorSensor.rgb) > 80:
                colors.append(1)
            else:
                colors.append(0)
        print(colors)
        determineType(box, colors)
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=45, sleep_time=0.01,brake=True)
        bothmotors.on_for_rotations(-10,-10,rotationsneeded*2)
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=-45, sleep_time=0.01,brake=True)
        bothmotors.on_for_rotations(-10,-10,rotationsneeded)
        

    else:
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=-180, sleep_time=0.01,brake=True)
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=45, sleep_time=0.01,brake=True)
        bothmotors.on_for_rotations(10,10,rotationsneeded)
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=-45, sleep_time=0.01,brake=True)
        print(averageRGB(colorSensor.rgb))
        print(colorSensor.reflected_light_intensity)
        while ((averageRGB(colorSensor.rgb) > 1 and averageRGB(colorSensor.rgb) < 5) or (averageRGB(colorSensor.rgb) < 80 and averageRGB(colorSensor.rgb) > 5)):
            print(averageRGB(colorSensor.rgb))
            bothmotors.on_for_rotations(10,10,0.01)
        if averageRGB(colorSensor.rgb) > 80:
                colors.append(1)
        else:
                colors.append(0)
        for i in range(3):
            bothmotors.on_for_rotations(10,10,0.075)
            if averageRGB(colorSensor.rgb) > 80:
                colors.append(1)
            else:
                colors.append(0)
        print(colors)
        determineType(box, colors)
        bothmotors.on_for_rotations(-10,-10,rotationsneeded)
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=45, sleep_time=0.01,brake=True)
        bothmotors.on_for_rotations(-10,-10,rotationsneeded)
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=-45, sleep_time=0.01,brake=True)
        bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=180, sleep_time=0.01,brake=True)
        bothmotors.on_for_rotations(10,10,0.35)
    correct()
def Pickup(box):
    if box[2] < 7:
        motorB.on_for_rotations(70,2)
        TurnClockwise(-90)
        #bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=-90)
        bothmotors.on_for_rotations(10,10,0.4)
        motorB.on_for_rotations(-50,2)
        bothmotors.on_for_rotations(-10,-10,0.6)
        motorB.on_for_rotations(70,2)
        bothmotors.on_for_rotations(10,10,0.3)
        TurnClockwise(90)
        #bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=90)
        correct()
    else:
        motorB.on_for_rotations(70,2)
        TurnClockwise(90)
        #bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=90)
        bothmotors.on_for_rotations(10,10,0.4)      
        motorB.on_for_rotations(-50,2)
        bothmotors.on_for_rotations(-10,-10,0.6)
        motorB.on_for_rotations(70,2)
        bothmotors.on_for_rotations(10,10,0.3)
        TurnClockwise(-90)
        #bothmotors.turn_degrees(speed=SpeedPercent(8), target_angle=-90)
        correct()
def Dropoff():
    bothmotors.on_for_rotations(-10,-10,1)
    motorB.on_for_rotations(-70,2.5)
    bothmotors.on_for_rotations(10,10,1)
def subtask1():
    boxnum = int(input("What box number are we assigned to ? : "))
    boxwidth = 6
    boxnum = boxnum-6
    MoveForward(36)
    TurnClockwise(90)
    MoveForward(4)
    MoveForward(boxwidth*boxnum-3)
    for i in range(5):
        motorB.on_for_seconds(20,0.5)
        motorB.on_for_seconds(-20,0.5)
    MoveForward(97-boxwidth*boxnum-6)
    TurnClockwise(90)
    MoveForward(34)
    correct()
def subtask2():
    TurnClockwise(180)
    MoveForward(13)
    TurnClockwise(-90)
    correct()
    MoveForward(96)
    TurnClockwise(-90)
    MoveForward(10)
def subtask3():
    MoveForward(22)
    ScanBarcode(['A', 1, 9,1])
def subtask4():
    Pickup(['A', 1, 9,1])
    MoveForward(68)
def main(task):
    if task ==1:
        subtask1()
    elif task==2:
        subtask2()
    elif task==3:
        subtask3()
    elif task ==4:
        subtask4()
    elif task ==5:
        MovementToBox(box)
        ScanBarcode(box)
        Pickup(box)
        MoveToFulfill(fulfillmentcenter)
        Dropoff()
        MoveToHome(fulfillmentcenter)
finalornot = int(input("What task are we running Subs(1,2,3,4) or Final(5)"))
main(finalornot)
