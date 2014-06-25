import RPi.GPIO as GPIO
import camera_action
import time

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
             GPIO.cleanup()
             exit()


sense_motion()
