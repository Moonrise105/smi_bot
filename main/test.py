from main import image, funcs
from PIL import Image
import requests
from bs4 import BeautifulSoup
import io

def parser():
    link = "https://yadi.sk/d/xSSpY0XDkwa26w"
    req = requests.get(link)
    soup = BeautifulSoup(req.text, features="html.parser")
    a = soup.find_all("span", class_="clamped-text")
    m = []
    for i in a:
        if (".jpg" in i.text.lower()) or (".png" in i.text.lower() or (
                ".jpeg" in i.text.lower())):
            new_link = link + "/" + i.text
            req1 = requests.get(new_link)
            # image_stream = io.BytesIO(req1.content)
            # image_to_send = Image.open(image_stream)
            soup1 = BeautifulSoup(req1.text, features="html.parser")
            b = soup1.find("div", class_="scalable-preview scalable-preview_active slider__preview").text

            print(b)

    print(a)
    print(m)
def pars():
    link = "https://s155vla.storage.yandex.net/rdisk/093a1ab55e2c7e17b311bfabb440431d01bfdb1d33677fc98e8b11a1c06ea5c8/5de82c82/vhRy8PCVLNhXR7Cqa9tCLBwspMmqtyY5QHxaJEKIHHB_JfBCaVAzyBS-p49SZDP8c8UZqywEcqY4EMFNfj_P3A==?uid=0&filename=IMG_8054.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&tknv=v2&owner_uid=105252908&fsize=3950614&hid=17269fb0167bcf5ff8ae0eaddbf1792e&media_type=image&etag=3ea140a492662179c3fbf8ceabf7d8cb&rtoken=hBRifuuuCOmD&force_default=no&ycrid=na-0f7b97eee57cb4d0e93c7c08561eabed-downloader1h&ts=598e7f122a480&s=76f4e70db816f81c3b23a94974c5ff9c913e36b658399770278cc4e272a7e596&pb=U2FsdGVkX1-Jyp78Jm-HtXw5zgRTBrGmjK53UcFDOJAvxGs_uCdsXiLHwyxrsR7RUxfNWYNKkmhc3u5FXZ7T2FymUSJgwHU10SkFPeNazIU"
    req = requests.get(link)
    image_stream = io.BytesIO(req.content)
    image_to_send = Image.open(image_stream)
    image_to_send.show()

#parser()
pars()
