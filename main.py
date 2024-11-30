import telebot
import webbrowser
from telebot import types
import sqlite3


token = '7842143617:AAEHbIGBUAklNmV4S-emSTvTYIlVxaT4lJ4'  # сюда вставьте свой токен
bot = telebot.TeleBot(token)

name1 = ''  # сюда будем сохранять имя пользователя


def create_db():
    conn = sqlite3.connect('database.sql')  # открываем подключение к БД
    cur = conn.cursor()  # создаем курсор
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, user_name varchar(50), password varchar(50))')  # запрос для создания таблицы users
    conn.commit()  # сохраняем изменения
    cur.execute("INSERT INTO users (user_name, password) VALUES ('aaa', 'bbb')")  # запрос для создания таблицы users
    cur.close()  # закрываем курсор
    conn.close()  # закрываем соединение


create_db()


# функция для получения имени, которое вписал пользователь
def get_name(message):
    global name1  # делаем возможность обращаться к внешней переменной name1
    name1 = message.text.strip()  # в эту переменную записываем то, что получили от пользователя, без пробелов до и после
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, get_password)


# функция для получения пароля и для записи пользователя в БД
def get_password(message):
    password1 = message.text.strip()
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    # вставка (name1, password1) в таблицу пользователей
    cur.execute("INSERT INTO users (user_name, password) VALUES ('%s', '%s')" % (name1, password1))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()  # место для кнопок возле сообщения
    # в InlineKeyboardButton обязательно передаём callback. Это функция, которая будет срабатывать при нажатии на
    # кнопку. И в этот callback кладём 'users'
    btn1 = types.InlineKeyboardButton("Список пользователей", callback_data='users')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)


@bot.message_handler(commands=['start'])
def new(message):
    markup = types.ReplyKeyboardMarkup()  # место для кнопок под полем для ввода сообщения
    # класс этих кнопок (KeyboardButton) отличается от кнопок возле сообщения (InlineKeyboardButton).
    # Тут callback передавать не надо, будем вызывать функцию on_click (см. 67, 71 стр) и там смотреть,
    # какую кнопку нажал пользователь
    btn1 = types.KeyboardButton("перейти в ВК")
    btn2 = types.KeyboardButton("отправь фото")
    btn3 = types.KeyboardButton("Список пользователей")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "Введи команду", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


# тут смотрим, какую кнопку нажал пользователь
def on_click(message):
    if message.text == "перейти в ВК":
        webbrowser.open("vk.com")
    elif message.text == "отправь фото":
        file = open('files/photo.jpg', 'rb')
        bot.send_photo(message.chat.id, file)
    elif message.text == "Список пользователей":
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")  # выбираем всех пользователей из БД
        users = cur.fetchall()  # сохраняем все значения в переменную
        cur.close()
        conn.close()

        # далее всех пользователей будем записывать в текстовую переменную info
        info = ''
        for user in users:
            info += f'Имя: {user[1]}, пароль: {user[2]}'
        bot.send_message(message.chat.id, info)


@bot.callback_query_handler(func=lambda callback: True)
def callback_func(callback):
    if callback.data == 'edit':
        bot.edit_message_text('aaaaaa', callback.message.chat.id, callback.message.id - 2)
    elif callback.data == 'send':
        bot.send_message(callback.message.chat.id, 'helloooooooooo')
    elif callback.data == "users":
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        conn.close()

        info = ''
        for user in users:
            info += f'Имя: {user[1]}, пароль: {user[2]}'
        bot.send_message(callback.message.chat.id, info)


@bot.message_handler(content_types=['sticker', 'voice'])
def get_photo(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("перейти в ВК")
    btn2 = types.KeyboardButton("отправь фото")
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id, 'nice', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


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