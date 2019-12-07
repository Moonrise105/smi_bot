import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
import io
from vk_api import VkUpload
from main import funcs


class VkBot:

    def __init__(self, token, group_id, config_path, database=None):
        self.token = token
        self.group_id = group_id
        self.vk = None
        self.long_poll = None
        self.vk_api = None
        self.database = database
        self.config_path = config_path
        self.menus = {}

    def init_server(self):
        self.vk = vk_api.VkApi(token=self.token)
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)
        self.vk_api = self.vk.get_api()

    def send_message(self, user_id, text):
        return self.vk_api.messages.send(user_id=user_id,
                                         message=text,
                                         v=5.50)

    def send_photo(self, user_id, image):
        upload = VkUpload(self.vk)

        f = io.BytesIO()
        image.save(f, format='png')
        f.seek(0)

        photo = upload.photo_messages(photos=f)[0]
        attachment = "photo{}_{}".format(photo['owner_id'], photo['id'])
        self.vk_api.messages.send(user_id=user_id,
                                  attachment=attachment,
                                  v=5.50)

    def send_button_from_file(self, user_id, text, button):
        return self.vk_api.messages.send(user_id=user_id,
                                         message=text,
                                         keyboard=open(button, "r", encoding="UTF-8").read(),
                                         v=5.50)

    def send_button(self, user_id, text, keyboard):
        return self.vk_api.messages.send(user_id=user_id,
                                         message=text,
                                         keyboard=keyboard,
                                         v=5.50)



