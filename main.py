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


def create_db():
    conn = sqlite3.connect('database.sql')  # открываем подключение к БД
    cur = conn.cursor()  # создаем курсор
    cur.execute(
            'CREATE TABLE IF NOT EXISTS words (id int auto_increment primary key, en_word varchar(50), ru_word varchar(50), transcription varchar(50))')
    conn.commit()
    cur.execute(
            'CREATE TABLE IF NOT EXISTS questions (id int auto_increment primary key, question varchar(50), answer varchar(50))')
    conn.commit()
    cur.close()  # закрываем курсор
    conn.close()  # закрываем соединение
    insert_into_words()


def get_question():
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer, wrong_answers FROM questions ORDER BY RANDOM() LIMIT 1")
    question_data = cursor.fetchone()
    conn.close()
    return question_data



def insert_into_words():
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    words = [("Apple", "Яблоко", "[æpl]"), ("School", "Школа", "[skuːl]") , ("Teacher", "Учитель", " [ˈtiːtʃə(r)]"),
             ("Sentence", "Предложение", "[ˈsentəns]"), ("Math", "Математика", "[mæθ]") , ("Weather", "Погода", "[ˈweðə]")]
    for word in words:
        conn = sqlite3.connect('database.sql')  # открываем подключение к БД
        cur.execute("INSERT INTO words (en_word, ru_word, transcription) VALUES ('%s','%s','%s')" % (word[0], word[1], word[2]))
        conn.commit()
    cur.close()  # закрываем курсор
    conn.close()  # закрываем соединение



def insert_into_questions():
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    questions = [("Перевод слова яблоко на английском?", "Apple"), ("Погода на английском - это ...?", "Weather"), ("По-английски учитель будет ...?", "Teacher"), ("Перевод слова школа на английском? ", "School"), ("По-английски математика - это ...?", "Math"), ("Слово предложение на английском переводится как ...?", "Sentence")]
    for question in questions:
        cur.execute(
            "INSERT INTO questions (question, answer) VALUES ('%s','%s')", (question[0], question[1]))
        conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    create_db()

bot.infinity_polling()
