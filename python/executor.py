from clarifai_logic import get_items_in_picture
from picture_logic import take_picture
import servo_movement
from firebase import initialize_firebase


def main():
    servo_movement.init()
    initialize_firebase()
    picture_name = take_picture()
    get_items_in_picture(picture_name)


if __name__ == "__main__":
    main()