# last updated 2/19/2024

import RPi.GPIO as GPIO
import time

servoPin = 18
st1 = 25
st2 = 8
st3 = 7
st4 = 1
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

GPIO.setup(st1, GPIO.OUT)
GPIO.setup(st2, GPIO.OUT)
GPIO.setup(st3, GPIO.OUT)
GPIO.setup(st4, GPIO.OUT)

GPIO.output(st1, GPIO.LOW)
GPIO.output(st2, GPIO.LOW)
GPIO.output(st3, GPIO.LOW)
GPIO.output(st4, GPIO.LOW)

stepperPins = [st1, st2, st3, st4]
seq = [[1,0,0,1],[1,1,0,0],[0,1,1,0],[0,0,1,1]]

def ledCtrl(mode):
	if mode == "on":
		GPIO.output(led, GPIO.HIGH)
	else:
		GPIO.output(led, GPIO.LOW)

def servoCtrl(cycle):
    # to use angle: angle/18 + 2
    servo.ChangeDutyCycle(cycle)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def stepperCtrl(dire, ang):
    steps = int((2048/360) * ang)
    stepCount = 0
    i = 0
    for i in range(steps):
        for pin in range(4):
            GPIO.output(stepperPins[pin], seq[stepCount][pin])
        if dire == "counter":
            stepCount = (stepCount - 1) % 4
        elif dire == "clock":
            stepCount = (stepCount + 1) % 4
        else:
            clean()
            break
        time.sleep(0.01)

def launchCtrl(mode):
    if mode == "y":
        launch.ChangeDutyCycle(7)
        time.sleep(0.4)
        launch.ChangeDutyCycle(0)
    elif mode == "r":
        launch.ChangeDutyCycle(5)
        time.sleep(0.4)
        launch.ChangeDutyCycle(0)

def clean():
    servo.stop()
    GPIO.output(stepperPins[0], GPIO.LOW)
    GPIO.output(stepperPins[1], GPIO.LOW)
    GPIO.output(stepperPins[2], GPIO.LOW)
    GPIO.output(stepperPins[3], GPIO.LOW)
    launch.stop()
    GPIO.cleanup()
    print("cleaned")

while True:
    GPIO.setmode(GPIO.BCM)
    component = input("led || servo || stepper || launch || clean: ")
    if component == "led":
        ledCtrl(input("Mode (on/off)"))
    elif component == "servo":
        servoCtrl(int(input("Cycle (1-15): ")))
    elif component == "stepper":
        stepperCtrl(input("Direction (clock/counter): "), int(input("Angle (degrees): ")))
    elif component == "launch":
        launchCtrl(input("Mode (y/r): "))
    else:
        clean()
        break 
clean()
