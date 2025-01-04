# 2/19/2024

import RPi.GPIO as GPIO
import time
import cv2
from datetime import datetime

GPIO.setmode(GPIO.BCM)

launchPin = 24

GPIO.setup(launchPin, GPIO.OUT)
launch = GPIO.PWM(launchPin, 50)
launch.start(0)
launch.ChangeDutyCycle(0)

#cam = cv2.VideoCapture("/dev/video0")
#cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
#vid_cod = cv2.VideoWriter_fourcc(*'XVID')
#output = cv2.VideoWriter("launchVid.mp4", vid_cod, 20.0, (640,480))

def recording():
    while True:
        ret,frame = cam.read()
        cv2.putText(frame, str(datetime.now()), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Camera", frame)
        output.write(frame)

def launching():
    while True:
        ans = input("Launch (y/n/r)? ")
        if ans == "y":
            launch.ChangeDutyCycle(7)
            #time.sleep(0.59) #for 360
            time.sleep(0.4)
            launch.ChangeDutyCycle(0)
            #launch.stop()
            print(str(datetime.now()))
        elif ans == "r":
            launch.ChangeDutyCycle(5)
            time.sleep(0.4)
            launch.ChangeDutyCycle(0)
        else:
            cam.release()
            output.release()
            break

while True:
    #ret,frame = cam.read()
    #cv2.putText(frame, str(datetime.now()), (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2, cv2.LINE_AA)
    #cv2.imshow("Camera", frame)
    #output.write(frame)
    ans = input("Launch (y/n/r)? ")
    if ans == "y":
        launch.ChangeDutyCycle(9)
        #time.sleep(0.59) #for 360
        time.sleep(0.4)
        launch.ChangeDutyCycle(0)
        #launch.stop()
        print(str(datetime.now()))
    elif ans == "r":
        launch.ChangeDutyCycle(5)
        time.sleep(0.4)
        launch.ChangeDutyCycle(0)
    else:
        break

#cam.release()
#output.release()
launch.stop()
GPIO.cleanup()
print("cleaned")
