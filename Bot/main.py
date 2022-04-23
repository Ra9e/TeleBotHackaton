import telebot
from googletrans import Translator
from gtts import gTTS
import sqlite3
import buttons
import config
from languages import Languages
import os

bot = telebot.TeleBot(config.TOKEN, parse_mode='HTML')

translator = Translator()


# Handling /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    firstname = message.from_user.first_name
    username = message.from_user.username
    chat_id = message.chat.id
    try:
        answer = f'<i>Привет {firstname} !</i>\n\nВыберите язык и напишите мне сообщение\n\nДоступные команды: /help'
        lang = bot.send_message(chat_id, answer, reply_markup=buttons.languages())

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(f"SELECT user_id FROM users WHERE user_id = ?", (chat_id,))
        data = cursor.fetchone()
        if data is None:
            cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", (firstname, username, chat_id, 'None', 'None',))
            conn.commit()
        else:
            pass
    except:
        pass

    conn.close()


# Handling /help command
@bot.message_handler(commands=['help'])
def help_command(message):
    msg_text = '\n\n<i>Available commands:</i>\n'
    msg_text += '<i>/language</i> - _Сменить язык_\n'
    msg_text += '<i>/help</i>> - _доступные команды_\n'
    msg_text += '<i>/statistics</i> - _Кол-во пользователей_'
    bot.reply_to(message, msg_text, reply_markup=buttons.delete())


# Handling /statistics command
@bot.message_handler(commands=['statistics'])
def stat_command(message):
    first_name = message.from_user.first_name
    chat_id = message.chat.id

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    num = cur.execute("SELECT COUNT(*) FROM users")
    for n in num:
        for i in n:
            msg_text = f'<i><i>Кол-во пользователей</i> - {i}</i>'

    conn.commit()
    conn.close()

    bot.send_message(chat_id, msg_text, parse_mode='html', reply_markup=buttons.delete())


# Handling /language command
@bot.message_handler(commands=['language'])
def lang_command(message):
    chat_id = message.chat.id
    try:
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT lang FROM users WHERE user_id = (?);", (chat_id,))
        data_lang = cur.fetchone()
        for lang in data_lang:
            answer = f'<i>Вы выбрали <i>{Languages[lang]}</i> язык.\n\n'
            answer += f'<i>Чтобы сменить, выберите новый язык</i>'
            bot.send_message(chat_id, answer, parse_mode='html', reply_markup=buttons.languages())
        conn.close()
    except:
        answer = f'Выберите язык'
        bot.send_message(chat_id, answer, parse_mode='html', reply_markup=buttons.languages())


# Callback Query Handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    firstname = call.message.chat.first_name
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    def save_language(short):
        bot.answer_callback_query(call.id, f'{Languages[call.data]} выбран язык. Отправь мне сообщение')
        cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', (call.data, chat_id,))
        conn.commit()
        text = f'<i>{Languages[call.data]} </i>выбран язык. Отправь мне сообщение'
        bot.edit_message_text(text, chat_id, call.message.id, reply_markup=buttons.settings())

    if call.data in ['en', 'ru', 'fr', 'de']:
        save_language(call.data)

    elif call.data == 'delete':
        try:
            bot.delete_message(chat_id, call.message.id)
            bot.delete_message(chat_id, call.message.id - 1)
        except:
            bot.answer_callback_query(call.id, 'oops!')

    elif call.data == 'settings':
        try:
            text = f'<i>Выберите новый язык</i>'
            bot.edit_message_text(text, chat_id, call.message.id, reply_markup=buttons.languages())
            bot.answer_callback_query(call.id, 'Settings')
        except:
            try:
                # If message is audio, edit_message_text() function don't work.
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, text, reply_markup=buttons.settings())
            except:
                bot.answer_callback_query(call.id, 'oops!')

    elif call.data == 'pronunciation':
        try:
            cursor.execute(f"SELECT lang FROM users WHERE user_id = ?", (chat_id,))
            data = cursor.fetchone()
            cursor.execute(f"SELECT result FROM users WHERE user_id = ?", (chat_id,))
            data_text = cursor.fetchone()
            for x in data_text:
                text = x
            for lang in data:
                result = translator.translate(text, dest=lang).text
                detect = translator.detect(text).lang
                try:
                    tts = gTTS(text=result, lang=lang, slow=False)
                    tts.save(f'{chat_id}.mp3')
                    bot.delete_message(chat_id, call.message.id)
                    caption = f'<i>Результат: </i>\n<b>{result.capitalize()}</b> \n\n<i>Определен:</i> __{detect}__ <i>to</i> __{lang}__'
                    bot.send_audio(chat_id, open(f'{chat_id}.mp3', 'rb'), caption=caption,
                                   reply_markup=buttons.result())
                    os.remove(f'{chat_id}.mp3')
                except:
                    bot.answer_callback_query(call.id, 'Неподдерживаемый язык')
        except:
            pass

    conn.close()


# Message handler
@bot.message_handler(content_types=['text', 'photo'])
def response(message):
    chat_id = message.chat.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if message.content_type == 'text':
        text = message.text

    # Save a text to db
    cursor.execute('UPDATE users SET result = (?) WHERE user_id = (?)', (text, chat_id,))
    conn.commit()

    cursor.execute(f"SELECT lang FROM users WHERE user_id = ?", (chat_id,))
    data = cursor.fetchone()
    cursor.execute(f"SELECT result FROM users WHERE user_id = ?", (chat_id,))
    data_text = cursor.fetchone()

    for x in data_text:
        text = x
    for lang in data:
        result = translator.translate(text, dest=lang).text

        detect = translator.detect(text).lang
        result = f'<i>Результат: </i>\n<b>{result.capitalize()}</b> \n\n<i>Определен:</i> __{detect}__ <i>в</i> __{lang}__'
        bot.send_message(chat_id, result, reply_markup=buttons.result())


bot.polling(none_stop=True)
