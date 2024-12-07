import telebot
import webbrowser
from telebot import types
import sqlite3


token = '7842143617:AAEHbIGBUAklNmV4S-emSTvTYIlVxaT4lJ4'  # сюда вставьте свой токен
bot = telebot.TeleBot(token)



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


def start():
    update.message.reply_text('Привет! Я бот для изучения языков. Используй команду /question, чтобы получить вопрос.')




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

# bot.polling(none_stop=True)
bot.infinity_polling()




