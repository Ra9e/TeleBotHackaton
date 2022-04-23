import telebot
from googletrans import Translator
from gtts import gTTS
import sqlite3
import buttons
import config
from languages import Languages
import os
import speech_recognition as sr
from pyffmpeg import FFmpeg
import time

bot = telebot.TeleBot(config.TOKEN, parse_mode='HTML')
recognizer = sr.Recognizer()
ff = FFmpeg()
translator = Translator()



# Handling /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    firstname = message.from_user.first_name
    lastname=""
    if message.from_user.last_name != None:
        lastname = message.from_user.last_name
    username = message.from_user.username
    chat_id = message.chat.id
    try:
        answer = f'<i>Привет,{firstname}{lastname}!</i>\n\nВыберите язык, напишите или отправьте голосовое сообщение\n\nДоступные команды: /help'
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



@bot.message_handler(commands=['help'])
def help_command(message):
    msg_text = '\n\n<i>Доступные команды:</i>\n'
    msg_text += '<i>/language</i> - Сменить язык\n'
    msg_text += '<i>/help</i> - Доступные команды\n'
    msg_text += '<i>/statistics</i> - Кол-во пользователей'
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
        bot.answer_callback_query(call.id, f'{Languages[call.data]} выбран язык. Отправь мне текстовое или голосовое сообщение')
        cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', (call.data, chat_id,))
        conn.commit()
        text = f'Выбран язык <i>{Languages[call.data]}</i>. Отправь мне текстовое или голосовое сообщение'
        bot.edit_message_text(text, chat_id, call.message.id, reply_markup=buttons.settings())

    if call.data in ['en', 'ru', 'fr', 'de', 'pl', 'it', 'ja', 'sk', 'tr', 'fi',
                     'kn','lv','az','sv','es','ko','da','el','et','sr',
                     'uz','hy','be','bg','is','ky','sl','so','tg','uk',]:
        save_language(call.data)

    elif call.data == "page_two":
        try:
            answer = f'Выберите язык и напишите мне сообщение\n\nДоступные команды: /help'
            bot.edit_message_text(answer, chat_id, call.message.id, reply_markup=buttons.page_two())
            bot.answer_callback_query(call.id, 'Выбор языка')
        except:
            pass

    elif call.data == "page_three":
        try:
            answer = f'Выберите язык и напишите мне сообщение\n\nДоступные команды: /help'
            bot.edit_message_text(answer, chat_id, call.message.id, reply_markup=buttons.page_three())
            bot.answer_callback_query(call.id, 'Выбор языка')
        except:
            pass

    elif call.data == "page_one":
        try:
            answer = f'Выберите язык и напишите мне сообщение\n\nДоступные команды: /help'
            bot.edit_message_text(answer, chat_id, call.message.id, reply_markup=buttons.languages())
            bot.answer_callback_query(call.id, 'Выбор языка')
        except:
            pass

    elif call.data == 'delete':
        try:
            bot.delete_message(chat_id, call.message.id)
            bot.delete_message(chat_id, call.message.id - 1)
        except:
            bot.answer_callback_query(call.id, 'Упс!')

    elif call.data == 'settings':
        try:
            text = f'Выберите язык и напишите мне сообщение\n\nДоступные команды: /help'
            bot.edit_message_text(text, chat_id, call.message.id, reply_markup=buttons.languages())
            bot.answer_callback_query(call.id, 'Выбор языка')
        except:
            try:
                # If message is audio, edit_message_text() function don't work.
                #bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, text, reply_markup=buttons.settings())
            except:
                bot.answer_callback_query(call.id, 'Упс!')

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
                    caption = f'<i>Результат: </i>\n<b>{result.capitalize()}</b> \n\n<i>Определен:</i> <b>{detect}</b> <i>в</i> <b>{lang}</b>'
                    bot.send_audio(chat_id, open(f'{chat_id}.mp3', 'rb'), caption=caption)
                    bot.send_message(chat_id, '<b>Продолжайте писать или нажмите:\n\n Также доступные команды: /help</b>', reply_markup=buttons.settings())
                    os.remove(f'{chat_id}.mp3')
                except:
                    bot.answer_callback_query(call.id, 'Неподдерживаемый язык')
        except:
            pass

    conn.close()


# Message handler
@bot.message_handler(content_types=['text'])
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
        result = f'<i>Результат: </i>\n<b>{result.capitalize()}</b> \n\n<i>Определен:</i> <b>{detect}</b> <i>в</i> <b>{lang}</b>'
        bot.send_message(chat_id,result)
        bot.send_message(chat_id,"Выберите действия или продолжите пользоваться переводчиком: ", reply_markup=buttons.result())

@bot.message_handler(content_types=['voice'])
def voice_response(message):
    chat_id = message.chat.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
      file_id = bot.get_file(message.voice.file_id)
      voice_file = bot.download_file(file_id.file_path)

      voice_file_path =str(file_id.file_unique_id) + ".ogg"

      with open(voice_file_path, 'wb') as new_file:
        new_file.write(voice_file)

      bot.reply_to(message, "Сообщение анализируется. Подождите...")
      time.sleep(2)

      converted_voice_file_path = str(file_id.file_unique_id) + "wavedition.wav"

      ff.convert(voice_file_path, converted_voice_file_path)

      with sr.WavFile(converted_voice_file_path) as voiceFile:
        audio = recognizer.record(voiceFile)

      query = recognizer.recognize_google(audio, language="ru-RU", show_all=False).lower()

      os.remove(voice_file_path)
      os.remove(converted_voice_file_path)

      bot.reply_to(message, query)

      cursor.execute('UPDATE users SET result = (?) WHERE user_id = (?)', (query, chat_id,))
      conn.commit()

      cursor.execute(f"SELECT lang FROM users WHERE user_id = ?", (chat_id,))
      data = cursor.fetchone()
      cursor.execute(f"SELECT result FROM users WHERE user_id = ?", (chat_id,))
      data_text = cursor.fetchone()

      for x in data_text:
          query = x
      for lang in data:
          result = translator.translate(query, dest=lang).text

          detect = translator.detect(query).lang

          result = f'<i>Результат: </i>\n<b>{result.capitalize()}</b> \n\n<i>Определен:</i> <b>{detect}</b> <i>в</i> <b>{lang}</b>'
          bot.send_message(chat_id, result)
          bot.send_message(chat_id, "Выберите действия или продолжите пользоваться переводчиком: ", reply_markup=buttons.result())

    except Exception as error:
      bot.reply_to(message, "Произошла ошибка, текст не распознан. Повторите...")
      os.remove(voice_file_path)
      os.remove(converted_voice_file_path)


bot.polling(none_stop=True)
