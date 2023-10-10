#!/usr/bin/env python3
"""
    From fulfillment area B, go to home area A.
"""
# Import needed robot output and inputs
from ev3dev2.motor import LargeMotor, MoveTank, MediumMotor, SpeedPercent
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_C, OUTPUT_B
from ev3dev2.sensor.lego import GyroSensor, InfraredSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from multiprocessing import pool
from final import MoveForward, TurnClockwise, MovementToBox, MoveToFulfill


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
#infrared = InfraredSensor(INPUT_2)
colorSensor = ColorSensor(INPUT_4)

# Constants needed for precise movement & turning
circumferenceOfTire = 6.775 #inches move forward in one rotation
rotationOfBMotor = 1.25
baseAngle = gyro.circle_angle()
speed = 20

#try get variables for more precise turning
initialAngle = gyro.circle_angle() #also initializes to 90 after reseting/calibrating
direction1 = initialAngle
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

def main():
    TurnClockwise(180)
    MoveForward(6)
    TurnClockwise(-90)
    MoveForward(90)
    TurnClockwise(-90)
    MoveForward(6)

main()