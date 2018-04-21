import serial

from python.TrashCategories import TrashCategories
from python.arduino_envs import ArduinoEnv

COMPOST_CONFIG = bytes([0])
LANDFILL_CONFIG = bytes([90])
RECYCLING_CONFIG = bytes([180])


def set_servos(can):
    arduino_serial_data = serial.Serial(ArduinoEnv.LOG_FILE, 9600)
    if can == TrashCategories.COMPOST:
        arduino_serial_data.write(COMPOST_CONFIG)
    elif can == TrashCategories.LANDFILL:
        arduino_serial_data.write(LANDFILL_CONFIG)
    else:
        arduino_serial_data.write(RECYCLING_CONFIG)
