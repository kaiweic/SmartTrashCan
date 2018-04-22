import os
import serial

from arduino_envs import ArduinoEnv


arduino_serial_data = serial.Serial('COM5', 9600)#, timeout=10)
print(arduino_serial_data)

while True:
    #print(arduino_serial_data.inWaiting())
    if arduino_serial_data.inWaiting():
        print("starting serial")
        converted_string = data.decode('utf-8').strip()
        print(converted_string)
        if converted_string[:len('SERIAL IS AVAILABLE')] == 'SERIAL IS AVAILABLE':
            print("getting serial data")
            os.system('python executor.py')
            break
        while arduino_serial_data.inWaiting():
            arduino_serial_data.readline()

