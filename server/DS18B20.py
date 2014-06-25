import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_directory = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_directory + '28*')[0]
device_file = device_folder + '/w1_slave'

'''
the file looks like this:
c3 01 4b 46 7f ff 0d 10 2f : crc=b4 YES
c3 01 4b 46 7f ff 0d 10 2f : t=28687

'''

def read_raw_temperature():
    raw_file = open(device_file, 'r')
    lines = raw_file.readlines()
    raw_file.close()
    return lines

def read_temperature():
    text = read_raw_temperature()
    while text[0].strip()[-3:] != 'YES':  #we check if we could read data from the sensor
        time.sleep(0.3) #wait a little to make other request
        text = read_raw_temperature()

    temperature_position = text[1].find('t=') # finds where temperature is written 
    
    if temperature_position != -1: #if we have found where the temerature is written
        temperature_string = text[1][temperature_position+2:] # so now we have 28687
        temperature_celsius = float(temperature_string)/1000.0
        temperature_fahrenheit = temperature_celsius * 9.0 / 5.0 + 32.0 # from wikipedia
        return temperature_celsius, temperature_fahrenheit 


read_temperature()
