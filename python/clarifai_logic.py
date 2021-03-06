import serial
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json

import env_vars, servo_movement
from TrashCategories import TrashCategories
from arduino_envs import ArduinoEnv
from firebase import update
from model.fullness_object import FullnessObject

recyclables = {"bottle", "plastic", "cup"}
compost = {"apple", "clementine", "orange", "fruit", "tangerine", "mandarin", "food", "vegetable", "coffee", "knife",
           "fork"}

app = ClarifaiApp(api_key=env_vars.clarifai_api_key)

def get_items_in_picture(filename, model_type=None):
    model = app.models.get('general-v1.3', model_type=model_type)
    img = ClImage(file_obj=open(filename, 'rb'))
    pred = model.predict([img])

    # 1. Recycling
    # 2. If recycling fails, compost
    # 3. Default to garbage
    is_recycling = False
    is_compost = False
    items = ""
    index = 0
    for item in pred['outputs'][0]['data']['concepts']:
        items += json.dumps(item['name'])[1:-1] + ", "

        if item['name'] in recyclables:
            is_recycling = True
            break
        elif item['name'] in compost:
            is_compost = True
            if index < 2:
                break

        index += 1

    print(items)

    if is_recycling:
        print("Recycle that shit!")
        servo_movement.set_servos(TrashCategories.RECYCLING)
    elif is_compost:
        print("Compost that shit!")
        servo_movement.set_servos(TrashCategories.COMPOST)
    else:
        print("Trash that shit!")
        servo_movement.set_servos(TrashCategories.LANDFILL)

    
   