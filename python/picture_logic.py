from cv2 import cv2


def take_picture():
    camera = cv2.VideoCapture(0)
    saved_image_name = 'trash_object.jpg'
    print(saved_image_name)

    while True:
        return_value, raw_image = camera.read()
        display_image = raw_image
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottom_left_corner_of_text = (350, 40)
        font_scale = 1
        font_color = (255, 255, 255)
        line_type = 2

        cv2.putText(display_image, 'Press Spacebar to take a picture',
                    bottom_left_corner_of_text,
                    font,
                    font_scale,
                    font_color,
                    line_type)

        cv2.imshow('image', display_image)
        if cv2.waitKey(1) & 0xFF == 32:
            cv2.imwrite(saved_image_name, raw_image)
            break

    camera.release()
    cv2.destroyAllWindows()
    return saved_image_name
