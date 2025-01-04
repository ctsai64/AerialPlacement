# Aerial Detection for Object Placement
# last updated 12/26/2023

import RPi.GPIO as GPIO
import time
import numpy
import math
import sys
sys.path.append("..")
from detector import detector
import position
import distance

servoPin = 18
stepperPins = [25, 8, 7, 1]
launchPin = 24
led = 22
button = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(button, GPIO.IN, GPIO.PUD_OFF)

GPIO.setup(servoPin, GPIO.OUT)
servo = GPIO.PWM(servoPin, 50)
servo.start(0)

GPIO.setup(launchPin, GPIO.OUT)
launch = GPIO.PWM(launchPin, 50)
launch.start(0)

GPIO.setup(stepperPins[0], GPIO.OUT)
GPIO.setup(stepperPins[1], GPIO.OUT)
GPIO.setup(stepperPins[2], GPIO.OUT)
GPIO.setup(stepperPins[3], GPIO.OUT)

GPIO.output(stepperPins[0], GPIO.LOW )
GPIO.output(stepperPins[1], GPIO.LOW )
GPIO.output(stepperPins[2], GPIO.LOW )
GPIO.output(stepperPins[3], GPIO.LOW )

# seq = [[1,0,0,1], [1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], [0,0,1,0], [0,0,1,1], [0,0,0,1]]
seq = [[1,0,0,1],[1,1,0,0],[0,1,1,0],[0,0,1,1]]

servoPos = 1
def servoCtrl(cycle):
    # to use angle: angle/18 + 2
    servo.ChangeDutyCycle(cycle)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

steps = 0
stepCount = 0
def stepperCtrl(angle):
    steps = (2048/360) * angle
    i = 0
    for i in range(steps):
        for p in range(4):
            GPIO.output(stepperPins[p], seq[stepCount][p])
            stepCount = (stepCount - 1) % 4
        time.sleep(0.01)

def clean():
    servo.stop()
    GPIO.output(stepperPins[0], GPIO.LOW)
    GPIO.output(stepperPins[1], GPIO.LOW)
    GPIO.output(stepperPins[2], GPIO.LOW)
    GPIO.output(stepperPins[3], GPIO.LOW)
    launch.stop()
    GPIO.cleanup()
    print("cleaned")

px = []
cm = []
eq = numpy.polyfit(px, cm, 2)

while True:
    servoCtrl(servoPos)
    GPIO.output(led, GPIO.HIGH)
    if GPIO.input(button) == GPIO.HIGH:
        GPIO.output(led, GPIO.LOW)
    while detector.returnResults == False:
        if servoPos <= 9:
            servoPos += 2
            servoCtrl(servoPos)
        else:
            GPIO.output(led, GPIO.HIGH)
            print("no cup found")
            break
    result = detector.returnResults()
    while result[3] > 330 and servoPos > 1:
        servoPos -= 1
        servoCtrl(servoPos)
        result = detector.returnResults()
    while result[3] < 310 and servoPos < 9:
        servoPos += 1
        servoCtrl(servoPos)
        result = detector.returnResults()
    distance = eq[0]*result[2][0]**2 + eq[1]*result[2][0] + eq[2]
    angle = math.acos(math.sqrt(96.04*math.pow(distance, 2)/(19.6*math.pow(5.928, 2)*0.4)))  
    stepperCtrl(angle)
    launch.ChangeDutyCycle(9)
    time.sleep(0.4)
    launch.ChangeDutyCycle(0)
    n = 0
    for n in range(steps):
        for p in range(4):
            GPIO.output(stepperPins[p], seq[stepCount][p])
            stepCount = (stepCount + 1) % 4
        time.sleep(0.01)
            
clean()
