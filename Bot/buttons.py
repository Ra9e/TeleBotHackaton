from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def languages():
    markup = InlineKeyboardMarkup()

    markup.row_width = 2
    markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="en"),
               InlineKeyboardButton("🇷🇺 Russian", callback_data="ru"),
               InlineKeyboardButton("🇫🇷 French", callback_data="fr"),
               InlineKeyboardButton("🇩🇪 German", callback_data="de"))

    return markup


def settings():
    markup = InlineKeyboardMarkup()

    btn2 = InlineKeyboardButton("Сменить язык", callback_data='settings')
    markup.add(btn2)

    return markup


def result():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("Произношение", callback_data='pronunciation')
    btn2 = InlineKeyboardButton("Настройки", callback_data='settings')
    btn = InlineKeyboardButton(" ❌ ", callback_data='delete')
    markup.add(btn1, btn2)
    markup.add(btn)

    return markup


def delete():
    markup = InlineKeyboardMarkup()

    btn = InlineKeyboardButton(" ❌ ", callback_data='delete')
    markup.add(btn)

    return markup
