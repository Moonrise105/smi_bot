import requests
import io
from main import vk_bot, image_exceptions, image, funcs, buttons_lib as bl
from vk_api.bot_longpoll import VkBotEventType
from PIL import Image
TEMPLATES_NAMES = ['АбитуриентЭМИТ', 'АктивистЭМИТ', 'АнонсЭМИТ',
                   'ВнеЭМИТ', 'ВыпусникЭМИТ',
                   'ЛичностьЭМИТ', 'НовостиЭМИТ',
                   'ПолезноеЭМИТ', 'ПослевкусиеЭМИТ',
                   'РаботягиЭМИТ', 'СтудСоветЭМИТ',
                   'УмныйЭМИТ', 'КарьераЭМИТ', 'ПреподавательЭМИТ']


class SmiBot(vk_bot.VkBot):

    def create_menus(self):
        logo_template_but1 = bl.Button("Лого", "default")
        logo_template_but2 = bl.Button("Шаблон", "default")
        processing_but1 = bl.Button("Обработка", "positive")
        cancel_but = bl.Button("Отмена", "negative")

        self.menus["logo_template"] = bl.Menu(onetime=False)
        self.menus["logo_template"].add_button(logo_template_but1, (0, 0))
        self.menus["logo_template"].add_button(logo_template_but2, (0, 1))
        self.menus["logo_template"].add_button(cancel_but, (1, 0))
        self.menus["logo_template"].update()

        self.menus["empty"] = bl.Menu(empty=True)

        self.menus["processing"] = bl.Menu(onetime=False)
        self.menus["processing"].add_button(processing_but1, (0, 0))
        self.menus["processing"].update()

        self.menus["cancel"] = bl.Menu(onetime=False)
        self.menus["cancel"].add_button(cancel_but, (0, 0))
        self.menus["cancel"].update()

    def start_server(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.object.from_id
                text = event.object.text
                state = self.database.request('''
                                              SELECT state FROM users
                                              WHERE user_id = {}
                                              '''.format(user_id),
                                              fetchall=True)

                if state is None:
                    self.first_message(user_id)
                elif state == 0:
                    if text.lower() == "обработка":
                        self.ask_logo_template(user_id)
                    else:
                        self.send_button(user_id, "Нажмите 'Обработка' для обработки фотографии.",
                                         self.menus["processing"].menu_json)
                else:
                    if text.lower() == "отмена":
                        self.cancel(user_id)
                    else:
                        if state == "wait_logo_or_template":
                            if text.lower() == "шаблон":
                                self.ask_template(user_id)
                            elif text.lower() == "лого":
                                self.ask_photo_for_logo(user_id)
                            else:
                                self.send_button(user_id, "Выберите: лого / шаблон",
                                                 self.menus["logo_template"].menu_json)
                        elif state == "wait_template":
                            self.ask_text(user_id, text)
                        elif state == "wait_text":
                            self.ask_blackout(user_id, text)
                        elif state == "wait_blackout":
                            if funcs.is_number(text) and (0 <= int(text) <= 10):
                                self.ask_photo(user_id, text)
                            else:
                                self.send_button(user_id, "Введите число от 0 до 10 ", self.menus["cancel"].menu_json)
                        elif state == "wait_photo":
                            self.create_photo(user_id, event)
                        elif state == "wait_photo_for_logo":
                            self.add_logo(user_id, event)

    def first_message(self, user_id):
        self.database.request('''
                                                  INSERT INTO users(user_id, state)
                                                  VALUES ({}, 0)
                                                  '''.format(user_id),
                              commit=True)
        self.send_button(user_id, "Нажмите 'Обработка' для обработки фотографии", self.menus["processing"].menu_json)

    def cancel(self, user_id):
        self.database.request('''
                                                                      UPDATE users 
                                                                      SET state = 0,
                                                                      template = 0,
                                                                      text_photo = 0,
                                                                      blackout = 0
                                                                      WHERE user_id = {}
                                                                      '''.format(user_id),
                              commit=True)
        self.send_button(user_id, "Нажмите 'Обработка' для обработки фотографии",
                         self.menus["processing"].menu_json)

    def add_logo(self, user_id, event):
        for attachment in event.object.attachments:
            try:
                if attachment['type'] != 'doc':
                    raise image_exceptions.WrongFormat
                image_url = attachment['doc']['url']
                photo = requests.get(image_url)
                image_to_send = image.add_logo(photo.content,
                                               funcs.get_setting(self.config_path,
                                                                 "path",
                                                                 "path_logo"),
                                               0.2)
                self.send_photo(user_id, image_to_send)
                self.database.request('''
                                                                              UPDATE users 
                                                                              SET state = 0,
                                                                              template = 0,
                                                                              text_photo = 0,
                                                                              blackout = 0
                                                                              WHERE user_id = {}
                                                                              '''.format(user_id),
                                      commit=True)
                self.send_button(user_id, "Нажмите 'Обработка' для обработки фотографии",
                                 self.menus["processing"].menu_json)
            except image_exceptions.WrongFormat:
                self.send_button(user_id,
                                 "Фото должно быть отправлено документом.",
                                 self.menus["cancel"].menu_json)

    def ask_logo_template(self, user_id):
        self.database.request('''
                                                              UPDATE users 
                                                              SET state = "wait_logo_or_template"
                                                              WHERE user_id = {}
                                                              '''.format(user_id),
                              commit=True)
        self.send_button(user_id, "Выберите: лого / шаблон", self.menus["logo_template"].menu_json)

    def ask_template(self, user_id):
        self.send_button(user_id, '''
                                                            Выберите хэштэг (введите число) или введите свой:
                                                            1 - АбитуриентЭМИТ
                                                            2 - АктивистЭМИТ
                                                            3 - АнонсЭМИТ
                                                            4 - ВнеЭМИТ
                                                            5 - ВыпусникЭМИТ
                                                            6 - ЛичностьЭМИТ
                                                            7 - НовостиЭМИТ
                                                            8 - ПолезноеЭМИТ
                                                            9 - ПослевкусиеЭМИТ
                                                            10 - РаботягиЭМИТ
                                                            11 - СтудСоветЭМИТ
                                                            12 - УмныйЭМИТ
                                                            13 - КарьераЭМИТ
                                                            14 - ПреподавательЭМИТ''',
                         self.menus["cancel"].menu_json)
        self.database.request('''
                                                      UPDATE users 
                                                      SET state = "wait_template"
                                                      WHERE user_id = {}
                                                      '''.format(user_id),
                              commit=True)

    def ask_text(self, user_id, text):
        self.send_button(user_id, "Введите текст.", self.menus["cancel"].menu_json)
        self.database.request('''
                                                      UPDATE users 
                                                      SET template = "{}"
                                                      WHERE user_id = {}
                                                      '''.format(text, user_id),
                              commit=True)
        self.database.request('''
                                                      UPDATE users 
                                                      SET state = "wait_text"
                                                      WHERE user_id = {}
                                                      '''.format(user_id),
                              commit=True)

    def ask_blackout(self, user_id, text):
        self.send_button(user_id, "Введите затемнение (целое число от 0 до 10)", self.menus["cancel"].menu_json)
        self.database.request('''
                                                                          UPDATE users 
                                                                          SET text_photo = '{}'
                                                                          WHERE user_id = {}
                                                                          '''.format(text.replace("\'", "\""), user_id),
                              commit=True)
        self.database.request('''
                                                                          UPDATE users 
                                                                          SET state = "wait_blackout"
                                                                          WHERE user_id = {}
                                                                          '''.format(user_id),
                              commit=True)

    def ask_photo(self, user_id, text):
        self.send_message(user_id, "Отправьте фото")
        self.database.request('''
                                                                              UPDATE users 
                                                                              SET blackout = {}
                                                                              WHERE user_id = {}
                                                                              '''.format(text, user_id),
                              commit=True)
        self.database.request('''
                                                                              UPDATE users 
                                                                              SET state = "wait_photo"
                                                                              WHERE user_id = {}
                                                                              '''.format(user_id),
                              commit=True)

    def ask_photo_for_logo(self, user_id):
        self.send_message(user_id, "Отправьте фото")
        self.database.request('''
                                                                                      UPDATE users 
                                                                                      SET state = "wait_photo_for_logo"
                                                                                      WHERE user_id = {}
                                                                                      '''.format(user_id),
                              commit=True)

    def create_photo(self, user_id, event):
        template_number = self.database.request('''
                                                                  SELECT template FROM users
                                                                  WHERE user_id = {}
                                                                  '''.format(user_id),
                                                fetchall=True)
        text_to_add = self.database.request('''
                                                                  SELECT text_photo FROM users
                                                                  WHERE user_id = {}
                                                                  '''.format(user_id),
                                            fetchall=True)
        blackout = self.database.request('''
                                                                          SELECT blackout FROM users
                                                                          WHERE user_id = {}
                                                                          '''.format(user_id),
                                         fetchall=True)
        for attachment in event.object.attachments:
            try:
                if attachment['type'] != 'doc':
                    raise image_exceptions.WrongFormat
                image_url = attachment['doc']['url']
                photo = requests.get(image_url)
                image_stream = io.BytesIO(photo.content)
                image_to_send = Image.open(image_stream)
                image_to_send = image.compression(image_to_send, (1500, 1000))
                if int(blackout) in range(2, 11):
                    image_to_send = image.change_brightness(image_to_send,
                                                            funcs.get_setting(self.config_path,
                                                                              "path",
                                                                              "path_bright"),
                                                            blackout)
                image_to_send = image.add_template(image_to_send,
                                                   funcs.get_setting(self.config_path,
                                                                     "path",
                                                                     "path_template"))
                if funcs.is_number(template_number) and int(template_number) in range(1, 15):
                    image_to_send = image.add_tag(image_to_send,
                                                  funcs.get_setting(self.config_path,
                                                                    "path",
                                                                    "path_font"),
                                                  '#' + TEMPLATES_NAMES[int(template_number) - 1],
                                                  46)
                else:
                    image_to_send = image.add_tag(image_to_send,
                                                  funcs.get_setting(self.config_path,
                                                                    "path",
                                                                    "path_font"),
                                                  str(template_number),
                                                  46)
                image_to_send = image.add_text(image_to_send,
                                               funcs.get_setting(self.config_path,
                                                                 "path",
                                                                 "path_font"),
                                               image.align_text(text_to_add, 14),
                                               105)
                # image_to_send = funcs.image_to_byte_array(image_to_send)
                self.send_photo(user_id, image_to_send)
                self.database.request('''
                                                              UPDATE users 
                                                              SET state = 0,
                                                              template = 0,
                                                              text_photo = 0,
                                                              blackout = 0
                                                              WHERE user_id = {}
                                                              '''.format(user_id),
                                      commit=True)
                self.send_button(user_id, "Нажмите 'Обработка' для обработки фотографии",
                                 self.menus["processing"].menu_json)
            except image_exceptions.SmallSize:
                self.send_button(user_id,
                                 "Маленький размер",
                                 self.menus["cancel"].menu_json)
            except image_exceptions.WrongRatio:
                self.send_button(user_id,
                                 "Неправильные пропорции (надо 3:2 или шире)",
                                 self.menus["cancel"].menu_json)
            except image_exceptions.WrongFormat:
                self.send_button(user_id,
                                 "Фото должно быть отправлено документом.",
                                 self.menus["cancel"].menu_json)
