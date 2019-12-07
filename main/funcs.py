import configparser
from PIL import Image
import io
import traceback
import datetime
import requests


def get_setting(path, section, setting):
    config = configparser.ConfigParser()
    config.read(path)
    value = config.get(section, setting)
    return value


def check_internet_connection(self):
    try:
        request = requests.get(url='https://vk.com/')
        if request.status_code == 200:
            return True
        else:
            return True
    except requests.exceptions.RequestException:
        return False


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


def write_log(path):
    with open(path, "a") as logs:
        logs.write(str(datetime.datetime.now()) + "\n" + traceback.format_exc() + "\n" + "_" * 80 + "\n")

