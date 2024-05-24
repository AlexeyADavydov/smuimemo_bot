import os
import logging

import telebot
from dotenv import load_dotenv
from telebot import types

from navigator import MAIN_CATEGORIES

load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

category = None

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s - %(levelname)s - %(message)s - %(name)s'
)


def buttons_generator(list_of_buttons):
    buttons = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    for i in list_of_buttons:
        buttons.add(
            types.KeyboardButton(i)
        )
    return buttons


@bot.message_handler(commands=['start'])
def start(message):
    buttons = buttons_generator(MAIN_CATEGORIES)
    bot.send_message(
        message.chat.id,
        f'Привет {message.from_user.first_name}! '
        f'Добро пожаловать в Архив опыта Совета молодых учёных ИМЭМО РАН! \n\n'
        f'Архив опыта создан для того, чтобы облегчить поиск '
        f'редкоиспользуемых, но важных бюрократических документов '
        f'или правил, которые в момент их необходимости '
        f'всегда неизвестно где находятся.\n\n'
        f'Архив включает шаблоны внешних писем, '
        f'рабочих материалов, служебных записок, '
        f'а также инструкции и просто документы, '
        f'где сохранен какой-то рабочий опыт. \n\n'
        f'Если у вас будут предложения по развитию и улучшению Архива опыта, '
        f'мы будем рады их услышать. Наша почта - smuimemo@yandex.ru',
        reply_markup=buttons
    )
    logging.info(
        f'ID:{message.from_user.id}, {message.from_user.username}'
    )


@bot.message_handler(func=lambda message: message.text == 'Назад')
def handle_personal_business(message):
    buttons = buttons_generator(MAIN_CATEGORIES)
    bot.send_message(
        message.chat.id,
        'Вы вернулись в основное меню',
        reply_markup=buttons
    )


@bot.message_handler(content_types=['text'])
def replies(message):
    global category

    if message.text in MAIN_CATEGORIES:
        category = MAIN_CATEGORIES[message.text]
        buttons = buttons_generator(category['name'])
        buttons.add(
            types.KeyboardButton('Назад')
        )
        description = category['description']
        bot.send_message(
            message.chat.id,
            f'{description}',
            reply_markup=buttons
        )

    elif message.text in category['name']:
        file_name = message.text
        path = category['path']
        file = open(
            file=f'{path}{file_name}',
            mode='rb'
        )
        bot.send_document(
            message.chat.id,
            document=file,
            caption=None
        )
        logging.info(
            f'{message.from_user.username} - {file_name}'
        )


if __name__ == "__main__":
    bot.polling()
