# last updated 2/19/2024

import RPi.GPIO as GPIO
import time

in1 = 25
in2 = 8
in3 = 7
in4 = 1

step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
alt_seq = [[1,0,0,1],[1,1,0,0],[0,1,1,0],[0,0,1,1]]

GPIO.setmode( GPIO.BCM )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )

GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()
    print("cleaned")
    
while True:
    dir = input("Direction (clock/counter): ")
    if dir == "clock" or dir == "counter":
        step_count = int((2048/360)*int(input("Angle (degrees): ")))
        i = 0
        for i in range(step_count):
            for pin in range(4):
                GPIO.output(motor_pins[pin], alt_seq[motor_step_counter][pin])
            if dir == "counter":
                motor_step_counter = (motor_step_counter - 1) % 4#8
            elif dir == "clock":
                motor_step_counter = (motor_step_counter + 1) % 4#8
            else:
                cleanup()
                break
            time.sleep(0.01) # min 0.002
    else:
        cleanup()
        break
cleanup()
exit( 0 )

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
# step_sleep = 0.002
# step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
# direction = False # True for clockwise, False for counter-clockwise
