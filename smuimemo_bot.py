
from dotenv import load_dotenv
import os
import telebot
from telebot import types


load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    buttons = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    buttons.add(
        types.KeyboardButton('Файл')
    )
    buttons.add(
        types.KeyboardButton('Сообщение')
    )
    bot.send_message(
        message.chat.id,
        f'Привет {message.from_user.first_name}',
        reply_markup=buttons
    )


@bot.message_handler(content_types=['text'])
def replies(message):
    if message.text == 'Файл':
        file = open(
            'requirements.txt',
            mode='r'
        )
        bot.send_document(
            message.chat.id,
            document=file,
            caption='Тестовый '
        )
    elif message.text == 'Сообщение':
        bot.send_message(
            message.chat.id,
            'Ответ бота',
        )

print('Бот запущен')
bot.polling(none_stop=True)
