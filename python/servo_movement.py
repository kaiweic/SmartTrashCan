import serial

from TrashCategories import TrashCategories
from arduino_envs import ArduinoEnv
from firebase import update
from model.fullness_object import FullnessObject

COMPOST_CONFIG = bytes([67])
LANDFILL_CONFIG = bytes([76])
RECYCLING_CONFIG = bytes([82])

arduino_serial_data = serial.Serial('COM5', 9600)#, timeout=1)

def init():
        arduino_serial_data.write(b'1');
        data = arduino_serial_data.readline()


def set_servos(can):
    print("in servo movement")
    if can == TrashCategories.COMPOST:
        print("in servo movement compost")
        print('compost: ', COMPOST_CONFIG)
        arduino_serial_data.write(COMPOST_CONFIG)
        # print(arduino_serial_data.read())
    elif can == TrashCategories.LANDFILL:
        print("in servo movement landfill")
        print("bytes written: ", arduino_serial_data.write(LANDFILL_CONFIG))
        print('landfill: ', LANDFILL_CONFIG)
        #print(arduino_serial_data.readline().decode('utf-8').strip())
        # print(str(arduino_serial_data.read()))
    else:
        print("in servo movement recycling")
        # arduino_serial_data.write(TrashCategories.RECYCLING.value.encode())
        arduino_serial_data.write(RECYCLING_CONFIG)
        # print(arduino_serial_data.readline())

    raw = arduino_serial_data.read()
    fullness_status = raw.decode('utf-8').strip()
    if (fullness_status == 'F'):
        raw = arduino_serial_data.read()
        fullness_status = raw.decode('utf-8').strip()
    print('updating', raw, fullness_status)
    update("can_1", FullnessObject(int(fullness_status) != 0))  # hard coding can id

