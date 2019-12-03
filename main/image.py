from PIL import Image, ImageDraw, ImageFont
from main import image_exceptions
import io


def add_logo(image, path_logo, logo_size):
    image_stream = io.BytesIO(image)
    main_image = Image.open(image_stream)
    logo = Image.open(path_logo)
    logo = logo.resize((int(main_image.size[1] * logo_size), int(main_image.size[1] * logo_size)), Image.ANTIALIAS)
    main_image.paste(logo, (main_image.size[0] - logo.size[0], main_image.size[1] - logo.size[1]), logo)
    return main_image


def proportional_compression(size, height):
    new_size = [0, 0]
    new_size[1] = height
    new_size[0] = int(new_size[1] / size[1] * size[0])
    return new_size


def compression(image, template_size):
    if image.size[0] < 1500 or image.size[1] < 1000:
        raise image_exceptions.SmallSize
    elif image.size[0] / image.size[1] < 1.5:
        raise image_exceptions.WrongRatio
    new_size = proportional_compression(image.size, 1000)
    if new_size[0] < 1500:
        raise image_exceptions.SmallWeightAfterCompression
    elif new_size[0] > 1500:
        image = image.resize(new_size, Image.ANTIALIAS)
        diff_size = (image.size[0] - template_size[0]) // 2
        image = image.crop((diff_size, 0, new_size[0] - diff_size, new_size[1]))
    else:
        image = image.resize(new_size, Image.ANTIALIAS)
    return image


def add_template(image, path_template):
    template = Image.open(path_template)
    if image.size[0] < 1500 or image.size[1] < 1000:
        raise image_exceptions.SmallSize
    elif image.size[0] / image.size[1] < 1.5:
        raise image_exceptions.WrongRatio
    new_size = proportional_compression(image.size, 1000)
    if new_size[0] < 1500:
        raise image_exceptions.SmallWeightAfterCompression
    elif new_size[0] > 1500:
        image = image.resize(new_size, Image.ANTIALIAS)
        diff_size = (image.size[0] - template.size[0]) // 2
        image.paste(template, (diff_size, 0), template)
        image = image.crop((diff_size, 0, new_size[0] - diff_size, new_size[1]))
    else:
        image = image.resize(new_size, Image.ANTIALIAS)
        image.paste(template, (0, 0), template)
    return image


def change_brightness(image, path_bright, blackout):
    blackout = Image.open(path_bright + "/" + str(blackout) + ".png")
    image.paste(blackout, (0, 0), blackout)
    return image


def align_text(text, max_symbols_in_row):
    text_list = str(text).split()
    new_text_list = []
    string = ""
    for word in text_list:
        if len(string) == 0 or (len(string) + len(word) <= max_symbols_in_row):
            string += word + " "
        else:
            new_text_list.append(string)
            string = word + " "
    if len(string) != 0:
        new_text_list.append(string)
    k = 0
    for i in new_text_list:
        new_text_list[k] = i.rstrip()
        k += 1
    return new_text_list


def add_text(image, path_font, text, font_size):
    k = 0
    indent = 0
    font = ImageFont.truetype(path_font, font_size)
    draw = ImageDraw.Draw(image)
    print(image.size)
    for row in text[::-1]:
        w, h = draw.textsize(row, font=font)
        if k != 0:
            indent = h
        pos_x = image.size[0] - w - 100
        pos_y = image.size[1] - 240 - indent * k
        draw.text((pos_x, pos_y), row, (255, 255, 255), font)
        k += 1
    return image


def add_tag(image, path_font, text, font_size):
    font = ImageFont.truetype(path_font, font_size)
    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(text, font=font)
    pos_x = image.size[0] - w - 100
    pos_y = image.size[1] - 100
    pos = (pos_x, pos_y)
    color = (255, 255, 255)
    draw.text(pos, text, color, font)
    return image
