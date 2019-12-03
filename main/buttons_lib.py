class Button:
    def __init__(self, label, color, type="text"):
        self.label = label
        self.color = color
        self.type = type
        self.button_json = self.create()

    def create(self):
        string = '''{
            "action": {
                "type": "%s",
                "label": "%s"
            },
            "color": "%s"
        }''' % (self.type, self.label, self.color)
        return string


class Menu:

    def __init__(self, onetime=False, empty=False):
        if empty:
            self.menu_json = '{"buttons":[],"one_time":true}'
        else:
            self.onetime = onetime
            self.buttons = [[None for i in range(5)] for i in range(10)]
            self.buttons_json = ""
            self.menu_json = ""

    def add_button(self, button, pos):
        self.buttons[pos[0]][pos[1]] = button

    def update(self):
        previous_list_added = False
        for line in self.buttons:
            element_added = False
            list_added = False
            for button in line:
                if button is not None:
                    if previous_list_added:
                        self.buttons_json += ","
                        previous_list_added = False
                    if element_added:
                        self.buttons_json += ','
                    if not list_added:
                        self.buttons_json += "["
                        list_added = True
                    self.buttons_json += (button.button_json + "\n")
                    element_added = True
            if list_added:
                self.buttons_json += "]"
                previous_list_added = True
        self.menu_json = '''
        {
            "one_time": %s,
            "buttons": [ %s 
            ]
        }
        ''' % (str(self.onetime).lower(), self.buttons_json)
        return self.menu_json
