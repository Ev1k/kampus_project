import sqlite3


def create_db():
    conn = sqlite3.connect('database.sql')  # открываем подключение к БД
    cur = conn.cursor()  # создаем курсор
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, user_name varchar(50), password varchar(50))')  # запрос для создания таблицы users
    conn.commit()  # сохраняем изменения
    cur.execute("INSERT INTO users (user_name, password) VALUES ('aaa', 'bbb')")  # вставка записей в таблицу users
    cur.close()  # закрываем курсор
    conn.close()  # закрываем соединение


create_db()
