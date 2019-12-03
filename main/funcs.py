import configparser
from PIL import Image
import io


def get_setting(path, section, setting):
    config = configparser.ConfigParser()
    config.read(path)
    value = config.get(section, setting)
    return value


def is_number(variable):
    try:
        int(variable)
        return True
    except ValueError:
        return False


def image_to_byte_array(image: Image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

