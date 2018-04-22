from python.clarifai_logic import get_items_in_picture
from python.firebase import initialize_firebase
from python.picture_logic import take_picture


def main():
    initialize_firebase()
    picture_name = take_picture()
    get_items_in_picture(picture_name)


if __name__ == "__main__":
    main()
