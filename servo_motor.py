# last updated 1/20/204

#3v3? power pin, output pin, gnd pin
import RPi.GPIO as GPIO
import time
pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)


#p.ChangeDutyCycle(5) #turn right by 90 deg
#time.sleep(0.5)
#p.ChangeDutyCycle(7.5)
#time.sleep(0.5)
#p.ChangeDutyCycle(10) #turn left by 19 deg
#time.sleep(0.5)
while True:
    go = input("Enter (x to exit): ") #1-15
    if go == "x":
        break
    else:
        p.ChangeDutyCycle(float(go))
        time.sleep(1)
        p.ChangeDutyCycle(0)
    #if go == "l":
    #    p.ChangeDutyCycle(10)
    #    time.sleep(0.23)
    #    p.ChangeDutyCycle(0)
    #elif go == "r":
    #    p.ChangeDutyCycle(5)
    #    time.sleep(0.23)
    #    p.ChangeDutyCycle(0)

p.stop()
GPIO.cleanup()
print("cleaned")

#from gpiozero import Servo
#from time import sleep

#servo = Servo(17)
#servo.value = None
#while True:
#    go = input("Where to?")
#    if go == "min":
#        servo.min()
#       servo.value = None
#       print("min")
 #   elif go =="mid":
 #       servo.mid()
#        servo.value = None
#        print("mid")
#    elif go == "max":
#        servo.max()
#        servo.value = None
#        print("max")
#    else:
#        nogo = int(go)
#        servo.value = nogo
#    servo.value = None   
