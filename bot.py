import traceback
import logging
import requests
from uuid import uuid4
import telebot
from telebot import types
from creds import TG_BOT_API
from speech import recognize
from ml import get_result, get_formatted_formula


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(TG_BOT_API, num_threads=10)

without_keyboard = types.ReplyKeyboardRemove(selective=False)


def retry(func):
    def wrapper(*args, **kwargs):
        need_retry = True
        retry_num = 0
        result = None
        while need_retry:
            try:
                result = func(*args, **kwargs)
                need_retry = False
            except Exception as e:
                retry_num += 1
                if retry_num >= 3:
                    print('*'*20 + ' ERROR ' + '*'*20)
                    traceback.print_exc()
                    need_retry = False
        return result
    return wrapper


def process(message):
    if message.voice:
        msg = 'Аудио не распознано'
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        url = 'https://api.telegram.org/file/bot{0}/{1}'.format(TG_BOT_API, file_info.file_path)
        r = requests.get(url)
        if r.status_code == 200:
            filename = str(uuid4())[:6] + '_' + file_info.file_path.split('/')[-1]
            filepath = 'audio/' + filename
            with open(filepath, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            data = recognize('audio', filename)
            if data:
                result = get_result(data)
                bot.send_message(message.from_user.id, 'Исходный текст: ' + data, reply_markup=without_keyboard, parse_mode='markdown')
                msg = get_formatted_formula(result)
            else:
                msg = 'Ошибка распознавания аудио'
    else:
        msg = 'Неизвестная команда'
    bot.reply_to(message, msg)
    bot.register_next_step_handler(message, process)


@bot.message_handler(commands=['start', 'help'])
@retry
def send_welcome(message):
    bot.send_message(message.from_user.id,
"""
Это бот для ClinicIQ, который распознаёт зубную формулу. Просто записываете аудио и отправляете, в ответ придёт формула.
Можно так же прислать forward аудио или загрузить файл.
""", parse_mode='markdown', reply_markup=without_keyboard)
    bot.register_next_step_handler(message, process)


@bot.message_handler(content_types=['audio', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
@retry
def default_command(message):
    return process(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
