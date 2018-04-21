from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json

from python import env_vars, servo_movement
from python.TrashCategories import TrashCategories

recyclables = {"bottle", "plastic"}
compost = {"apple", "clementine", "orange", "fruit", "tangerine", "mandarin", "food"}
landfill = {"phone", "wrapper"}


def get_items_in_picture(filename, model_type=None):
    app = ClarifaiApp(api_key=env_vars.clarifai_api_key)
    model = app.models.get('general-v1.3', model_type=model_type)
    img = ClImage(file_obj=open(filename, 'rb'))
    pred = model.predict([img])
    items = ""
    for item in pred['outputs'][0]['data']['concepts']:
        items += json.dumps(item['name'])[1:-1] + ", "

        if item['name'] in recyclables:
            print("Recycle that shit!")
            servo_movement.set_servos(TrashCategories.RECYCLING)
            break
        elif item['name'] in compost:
            print("Compost that shit!")
            servo_movement.set_servos(TrashCategories.COMPOST)
            break
        elif item['name'] in landfill:
            print("Trash that shit!")
            servo_movement.set_servos(TrashCategories.LANDFILL)
            break
        else:
            print("Defaulting to Trash that shit!")
            servo_movement.set_servos(TrashCategories.LANDFILL)

    print(items)

