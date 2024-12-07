import telebot
import webbrowser
from telebot import types
import sqlite3

token = '7842143617:AAEHbIGBUAklNmV4S-emSTvTYIlVxaT4lJ4'  # сюда вставьте свой токен
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['hello', 'start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Начать тест', callback_data='start-test')
    button2 = types.InlineKeyboardButton('Показать перевод слова', callback_data='show_translation') # func='edit'
    markup.add(button1, button2)
    bot.send_message(message.chat.id,"Привет, давайте приступим изучать иностранные языки.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handling_buttons(call):
    if call.data != "start-test":
        bot.send_message(call.message.chat.id, "yes")




# bot.polling(none_stop=True)
bot.infinity_polling()
