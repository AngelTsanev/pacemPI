import RPi.GPIO as GPIO
import camera_action
import time
import os

def sense_motion():
    GPIO.setmode(GPIO.BOARD)

    pir = 8
    #led = 12
    iterations = 0

    GPIO.setup(pir, GPIO.IN)  #activate input
    #GPIO.setup(led, GPIO.OUT) #activete output

    time.sleep(10)

    while (iterations < 36000):
        try:
            if GPIO.input(pir):
                #GPIO.output(led, GPIO.HIGH)
                camera_action.alert()
                print("Master, I sense motion in your room!")
            else:
                #GPIO.output(led, GPIO.LOW)
                print("Nothing to worry about.")
            time.sleep(1)
            iterations+=1

        except KeyboardInterrupt:
             print(" Quit")
             os.system("nohup raspistill -w 640 -h 480 -q 20 -o /tmp/stream/pic.jpg -tl 50 -t 9999999 > /dev/null 2>&1 & ")
             GPIO.cleanup()
             exit()


sense_motion()
