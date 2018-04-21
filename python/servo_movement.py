import serial

from python.TrashCategories import TrashCategories
from python.arduino_envs import ArduinoEnv


def set_servos(can):
    arduino_serial_data = serial.Serial(ArduinoEnv.LOG_FILE, 9600)
    if can == TrashCategories.COMPOST:
        arduino_serial_data.write(TrashCategories.COMPOST)
    elif can == TrashCategories.LANDFILL:
        arduino_serial_data.write(TrashCategories.LANDFILL)
    else:
        arduino_serial_data.write(TrashCategories.RECYCLING)
