from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def languages():
    markup = InlineKeyboardMarkup()

    markup.row_width = 2
    markup.add(InlineKeyboardButton("🇬🇧 Английский", callback_data="en"),
               InlineKeyboardButton("🇷🇺 Русский", callback_data="ru"),
               InlineKeyboardButton("🇫🇷 Французский", callback_data="fr"),
               InlineKeyboardButton("🇩🇪 Немецкий", callback_data="de"),
               InlineKeyboardButton("🇵🇱 Польский", callback_data="pl"),
               InlineKeyboardButton("🇮🇹 Итальянский", callback_data="it"),
               InlineKeyboardButton("🇯🇵 Японский", callback_data="ja"),
               InlineKeyboardButton("🇸🇰 Словацкий ", callback_data="sk"),
               InlineKeyboardButton("🇹🇷 Турецкий", callback_data="tr"),
               InlineKeyboardButton("🇫🇮 Финский", callback_data="fi"),
               InlineKeyboardButton("Вперёд", callback_data="page_two"))

    return markup


def page_two():
    markup = InlineKeyboardMarkup()

    markup.row_width = 2
    markup.add(InlineKeyboardButton("🇨🇦 Канадский", callback_data="kn"),
               InlineKeyboardButton("🇱🇻 Латышский", callback_data="lv"),
               InlineKeyboardButton("🇦🇿 Азербайджанский", callback_data="az"),
               InlineKeyboardButton("🇸🇪 Шведский", callback_data="sv"),
               InlineKeyboardButton("🇪🇸 Испанский", callback_data="es"),
               InlineKeyboardButton("🇰🇷 Корейский", callback_data="ko"),
               InlineKeyboardButton("🇩🇰 Датский", callback_data="da"),
               InlineKeyboardButton("🇬🇷 Греческий", callback_data="el"),
               InlineKeyboardButton("🇪🇪 Эстонский", callback_data="et"),
               InlineKeyboardButton("🇪🇪 Сербский", callback_data="sr"),
               InlineKeyboardButton("Назад", callback_data="page_one"),
               InlineKeyboardButton("Вперед", callback_data="page_three"),
               )

    return markup


def page_three():
    markup = InlineKeyboardMarkup()

    markup.row_width = 2
    markup.add(InlineKeyboardButton("🇺🇿 Узбекский", callback_data="uz"),
               InlineKeyboardButton("🇦🇲 Армянский", callback_data="hy"),
               InlineKeyboardButton("🇧🇾 Белорусский", callback_data="be"),
               InlineKeyboardButton("🇧🇬 Болгарский", callback_data="bg"),
               InlineKeyboardButton("🇮🇸 Исландский", callback_data="is"),
               InlineKeyboardButton("🇰🇬 Киргизский", callback_data="ky"),
               InlineKeyboardButton("🇸🇮 Словенский", callback_data="sl"),
               InlineKeyboardButton("🇸🇴 Сомали", callback_data="so"),
               InlineKeyboardButton("🇹🇯 Таджикский", callback_data="tg"),
               InlineKeyboardButton("🇺🇦 Украинский", callback_data="uk"),
               InlineKeyboardButton("Назад", callback_data="page_two")
               )

    return markup


def settings():
    markup = InlineKeyboardMarkup()

    btn2 = InlineKeyboardButton("Сменить язык", callback_data='settings')
    markup.add(btn2)

    return markup


def dictionary():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("Произношение", callback_data='pronunciation')
    btn2 = InlineKeyboardButton("Сменить язык", callback_data='settings')
    markup.add(btn1, btn2)

    return markup

def result():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("Произношение", callback_data='pronunciation')
    btn2 = InlineKeyboardButton("Сменить язык", callback_data='settings')
    btn3 = InlineKeyboardButton("Словарь", callback_data='dictionary')
    markup.add(btn1, btn2, btn3)

    return markup


def delete():
    markup = InlineKeyboardMarkup()

    btn = InlineKeyboardButton("Закрыть", callback_data='delete')
    markup.add(btn)

    return markup
