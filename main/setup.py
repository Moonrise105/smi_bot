from main import funcs, bot_smi, database


config_path = "C:/Users/-/PycharmProjects/smi_bot/main/settings/config"

if __name__ == "__main__":
    db_smi = database.DataBase(funcs.get_setting(config_path, "db", "host"),
                               funcs.get_setting(config_path, "db", "name"),
                               funcs.get_setting(config_path, "db", "user"),
                               funcs.get_setting(config_path, "db", "password"))
    bot = bot_smi.SmiBot(token=funcs.get_setting(config_path, 'vk', 'token'),
                         group_id=funcs.get_setting(config_path, 'vk', 'group_id'),
                         config_path=config_path,
                         database=db_smi)
    db_smi.connect()
    bot.init_server()
    bot.create_menus()
    bot.start_server()
