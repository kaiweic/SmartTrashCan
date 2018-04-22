import serial

from python.TrashCategories import TrashCategories
from python.arduino_envs import ArduinoEnv

COMPOST_CONFIG = bytes([0])
LANDFILL_CONFIG = bytes([90])
RECYCLING_CONFIG = bytes([180])


def set_servos(can):
    arduino_serial_data = serial.Serial(ArduinoEnv.LOG_FILE.value, 9600, timeout=1)
    print("in servo movement")
    if can == TrashCategories.COMPOST:
        print("in servo movement compost")
        arduino_serial_data.write(COMPOST_CONFIG)
        # print(arduino_serial_data.read())
    elif can == TrashCategories.LANDFILL:
        print("in servo movement landfill")
        arduino_serial_data.write(LANDFILL_CONFIG)
        # print(str(arduino_serial_data.read()))
    else:
        print("in servo movement recycling")
        # arduino_serial_data.write(TrashCategories.RECYCLING.value.encode())
        arduino_serial_data.write(RECYCLING_CONFIG)
        # print(arduino_serial_data.readline())
