from python.clarifai_logic import get_items_in_picture
from python.picture_logic import take_picture


def main():
    picture_name = take_picture()
    get_items_in_picture(picture_name)


if __name__ == "__main__":
    main()
