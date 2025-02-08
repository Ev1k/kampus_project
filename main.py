import telebot
import webbrowser
from telebot import types
import sqlite3

token = '7842143617:AAEHbIGBUAklNmV4S-emSTvTYIlVxaT4lJ4'  # сюда вставьте свой токен
bot = telebot.TeleBot(token)

right_word = "family"
next_question = "sdfgh"
correct_answers = 0

@bot.message_handler(commands=['hello', 'start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Начать тест', callback_data='start-test')
    button2 = types.InlineKeyboardButton('Показать перевод слова', callback_data='show_translation') # func='edit'
    markup.add(button1, button2)
    bot.send_message(message.chat.id,"Привет, давайте приступим изучать иностранные языки.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handling_buttons(call):
    if call.data == "start-test":
        bot.send_message(call.message.chat.id, "Как переводится слово семья?")
        bot.register_next_step_handler(call.message, check_answer)
    if call.data == "show_translation":
        bot.send_message(call.message.chat.id, "Показать перевод слова?")
        bot.register_next_step_handler(call.message, translate)

def check_answer(message):
    global right_word, correct_answers
    if message.text.strip().lower() == right_word:
        correct_answers +=1
        if correct_answers == 5:
            bot.send_message(message.chat.id, "Yes. That's right. Вы завершили тест")
        else:
            bot.send_message(message.chat.id, f"Yes. That's right.{next_question}")
            right_word = "apple"
            bot.register_next_step_handler(message, check_answer)
    else:
        bot.reply_to(message, "Неверно.Попробуй еще раз.")
        bot.register_next_step_handler(message, check_answer)
        if correct_answers == 5:
            bot.send_message(message.chat.id, "Вы завершили тест")

def translate(message):
    global right_word, correct_answers
    if message.text.strip().lower() == right_word:
        bot.send_message(message.chat.id, "family")







# bot.polling(none_stop=True)
bot.infinity_polling()
