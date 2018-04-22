import serial
import time

arduino_serial_data = serial.Serial('COM5', 9600)

print('bytes wrote: ', arduino_serial_data.write(b'd'))
arduino_serial_data.read()


for i in range(48, 58):
    print('sleeping')
    time.sleep(10)
    print('bytes wrote: ', arduino_serial_data.write(bytes([i])))
    print("send data")
    
    print(arduino_serial_data.read())
