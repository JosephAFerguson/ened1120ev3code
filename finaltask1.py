#!/usr/bin/env python3
"""
    Go to box location (ranging from A1_7-12), stop for 5 seconds, then
    proceed to fulfillment area B(2).
"""
# Import needed robot output and inputs
from ev3dev2.motor import LargeMotor, MoveTank, MediumMotor, SpeedPercent
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_C, OUTPUT_B
from ev3dev2.sensor.lego import GyroSensor, InfraredSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from multiprocessing import pool
from final import MoveForward, TurnClockwise


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

boxnum = int(input("What box number are we assigned to ? : "))
boxwidth = 6
boxnum = boxnum-6
def main():
    MoveForward(40)
    TurnClockwise(90)
    MoveForward(6)
    MoveForward(boxwidth*boxnum)
    for i in range(5):
        motorB.on_for_seconds(1,0.5)
        motorB.on_for_seconds(-1,0.5)
    MoveForward(96-boxwidth*boxnum-6)
    TurnClockwise(90)
    MoveForward(34)
main()