import json
from os.path import exists

import telebot
from telebot import types

from parsing import main, today, get_description

token = '6282091587:AAFAoNwDGoYRLSAwGd9ZS9Kvv39_JEeK0eo'

bot = telebot.TeleBot(token)

def get_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    with open(f'news_{today}.json', 'r') as file:
        for number, news in enumerate(json.load(file)):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=news['title'],
                    callback_data=str(number)
                )
            )
    return keyboard




@bot.message_handler(commands=['start', 'hi'])
def start_bot(message: types.Message):
    main()
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Новости на сегодня: ', reply_markup=get_keyboard())


@bot.callback_query_handler(func=lambda callback: True)
def send_news_detail(callback: types.CallbackQuery):
    with open(f'news_{today}.json', 'r') as file:
        news = json.load(file)[int(callback.data)]
        text = f"{news['title']}\n{get_description(news['news_link'])}\n\n{news['news_link']}"
        bot.send_message(
            callback.message.chat.id,
            text=text
        )


bot.polling()


# TODO: поправить создание файла
# TODO: При нажатии на кнопку «Quit» бот должен
# отправить сообщение “До свидания“

