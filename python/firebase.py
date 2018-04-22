import pyrebase

from env_vars import firebase_api_key

firebase = None
db = None


def initialize_firebase():
    config = {
        "apiKey": firebase_api_key,
        "authDomain": "smarttrashcan-a731b.firebaseapp.com",
        "databaseURL": "https://smarttrashcan-a731b.firebaseio.com",
        "projectId": "smarttrashcan-a731b",
        "storageBucket": "smarttrashcan-a731b.appspot.com",
        "messagingSenderId": "644066905865"
    }
    global firebase
    global db
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()


def build_firebase_record_object(fullness_object, trash_category):
    record_map = {
        "usage_list": [
            {
                "is_full": fullness_object.is_full,
                "timestamp": fullness_object.timestamp
            }
        ],
        "current_max_index": 0,
        "current_fullness": {
            "is_full": fullness_object.is_full,
            "timestamp": fullness_object.timestamp
        },
        "trash_category": trash_category
    }
    return record_map


def put_new_can_in_database(can_id, record_object):
    if firebase is None:
        raise ValueError("You forgot to initialize firebase, please call the initialize_firebase() function")
    if record_object is None:
        raise ValueError("Record object isn't proper")
    db.child(can_id).set(record_object)


def update(can_id, fullness_object):
    fullness_object_record = {
        "is_full": fullness_object.is_full,
        "timestamp": fullness_object.timestamp
    }
    current_num_in_usage_list = db.child(can_id).child("current_max_index").get().val()
    current_num_in_usage_list += 1
    db.child(can_id).child("current_max_index").set(current_num_in_usage_list)
    db.child(can_id).child("current_fullness").set(fullness_object_record)
    db.child(can_id).child("usage_list").child(current_num_in_usage_list).set(fullness_object_record)
