import smbus
import RPi.GPIO as GPIO
import time

def led_blink(position_on_gpio):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(position_on_gpio, GPIO.OUT) #setup

    GPIO.output(position_on_gpio, True)  #turns it on
    time.sleep(0.50)                     #during the sleep the led is glowing
    GPIO.output(position_on_gpio, False) #turns it off

    GPIO.cleanup() #cleanup

def tmp102_read_temperature(): #we read from two tmp102 sensor, we return the average value
    bus = smbus.SMBus(1)
    raw_temperature_first_sensor  = bus.read_i2c_block_data(0x48, 0)
    raw_temperature_second_sensor = bus.read_i2c_block_data(0x49, 0)
    #msb = most significant bit 
    msb_first_sensor  = raw_temperature_first_sensor[0]
    msb_second_sensor = raw_temperature_second_sensor[0]
    #lsb = least significant bit
    lsb_first_sensor  = raw_temperature_first_sensor[1]
    lsb_second_sensor = raw_temperature_second_sensor[1]
    #Make the led  blink, but we will need to execute with sudo
    #led_blink(12)
    first_temperature  = (((msb_first_sensor << 8) | lsb_first_sensor) >> 4) * 0.0625
    second_temperature = (((msb_second_sensor << 8) | lsb_second_sensor) >> 4) * 0.0625
    return (first_temperature + second_temperature) / 2.0
    
print("Temperature is : %.3f" % tmp102_read_temperature())

