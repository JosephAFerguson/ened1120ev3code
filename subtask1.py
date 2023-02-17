#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveTank
from ev3dev2.motor import OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import INPUT_1
motor1 = LargeMotor(OUTPUT_A)
motor2 = LargeMotor(OUTPUT_D)
bothmotors = MoveTank(OUTPUT_A, OUTPUT_D)
gyro = GyroSensor(INPUT_1)
radiusofTire = 30
switch = True

# command for run, brickrun -r ./codes/enedrobotcode.py
def movesubtask1a(distanceCM, n):
    for i in range(n):
        rotationsneeded = distanceCM / radiusofTire
        bothmotors.on_for_rotations(40,40,rotationsneeded)
        bothmotors.on_for_rotations(-40,-40,rotationsneeded)
def movesubtask1b(distanceCM, n, switch):
    for i in range(n*2):
        rotationsneeded = distanceCM / radiusofTire
        bothmotors.on_for_rotations(40,40,rotationsneeded)
        turn(switch)
        if switch == True:
            switch = False
        else:
            switch = True

initialangle  = gyro.circle_angle()
initialangleback = 0
if initialangle < 180:
    initialangleback = initialangle + 180
else:
    initialangleback = 360-initialangle
def turn(switch):
    angleneeded = 0
    currentangle = gyro.circle_angle()
    if switch == True:
        angleneeded = initialangleback
    else:
        angleneeded = initialangle
    upper = angleneeded + 5
    lower = angleneeded - 5
    while currentangle > upper or currentangle < lower:
        bothmotors.on_for_rotations(50,-60, 0.05)
        currentangle = gyro.circle_angle()


def b(switch):
    try:
        N = int(input("How many laps need done"))
        distanceForward = int(input("How many cm do you want to travel"))
        movesubtask1b(distanceForward, N, switch)
    except:
        return 1
    return 0
def a():
    try:
        N = int(input("How many laps need done"))
        distanceForward = int(input("How many cm do you want to travel"))
        movesubtask1a(distanceForward, N)
    except:
        return 1
    return 0

#for trial and error purposes
currtask = int(input("Select 1 for part a, 2 for part b"))
if currtask == 2:
    print(b(switch))
else:
    print(a())