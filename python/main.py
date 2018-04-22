import os
import serial

from python.arduino_envs import ArduinoEnv


arduino_serial_data = serial.Serial(ArduinoEnv.LOG_FILE.value, 9600, timeout=1)

while True:
    if arduino_serial_data.inWaiting():
        data = arduino_serial_data.readline()
        print("starting serial")
        converted_string = data.decode('utf-8').strip()
        print(converted_string)
        if converted_string[:len('SERIAL IS AVAILABLE')] == 'SERIAL IS AVAILABLE':
            print("getting serial data")
            os.system('python3 python/executor.py')
            break
        while arduino_serial_data.inWaiting():
            arduino_serial_data.readline()
