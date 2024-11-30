import telebot
import webbrowser
from telebot import types
import sqlite3

token = '7842143617:AAEHbIGBUAklNmV4S-emSTvTYIlVxaT4lJ4'  # сюда вставьте свой токен
bot = telebot.TeleBot(token)

name1 = ''  # сюда будем сохранять имя пользователя


# @bot.message_handler(commands=['hello', 'start'])
# def start(message):
#     markup = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton('go to site', url='vk.com')
#     button2 = types.InlineKeyboardButton('изменить текст', callback_data='edit') # func='edit'
#     button2 = types.InlineKeyboardButton('отправить сообщ', callback_data='send') # func='edit'
#     markup.add(button1, button2)
#     bot.send_message(message.chat.id, message.from_user.first_name, reply_markup=markup)


@bot.message_handler(commands=['info'])
def start(message):
    bot.send_message(message.chat.id, "<b>Help</b> <em>information</em>", parse_mode='html')


@bot.message_handler(commands=['site', 'website'])
def start(message):
    webbrowser.open('vk.com')


@bot.message_handler()
def text(message):
    if message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока')
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'привет')


# bot.polling(none_stop=True)
bot.infinity_polling()