import telebot
from telebot import types
from dotenv import load_dotenv
import psycopg2
import os
import csv
from pathlib import Path
load_dotenv()

token = os.getenv("TOKEN")
bot = telebot.TeleBot(token)

import sqlite3

# connection = sqlite3.connect("database.db", check_same_thread=False)
# cursor = connection.cursor()


connection = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("USER"),
                        password=os.getenv("PASSWORD"), host=os.getenv("HOST")) #(localhost)
cursor = connection.cursor()


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT, user_name TEXT, user_surname TEXT, username TEXT)")
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()

    if not row:
        cursor.execute("INSERT INTO users (user_id, user_name, user_surname, username)  VALUES (%s, %s, %s, %s)",
                       (user_id, user_name, user_surname, username))

    connection.commit()


@bot.message_handler(commands=['start'])  # создаем команду
def start(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Презентация",
                                         url='https://drive.google.com/file/d/1TJDsQ9-HXVjvcwMPcCqHb_4L7oc9Gn3n/view?usp=sharing')

    markup.add(button1)

    if message.from_user.id == 282163762: # or message.from_user.id==6372488471:
        button2 = types.InlineKeyboardButton(text='Показать всех users', callback_data='send_file')
        markup.add(button2)

    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт".format(message.from_user),
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "send_file")
def button_pressed_handler(call):
    cursor.execute("SELECT * FROM users")
    lines = cursor.fetchall()

    with open("users.csv", "w", encoding='utf-8') as f:
        file_writer = csv.writer(f, delimiter=",", lineterminator="\r")
        file_writer.writerow(["user_id", "first_name", "last_name", "username"])
        for line in lines:
            file_writer.writerow(line)

    dir_path = Path.cwd()
    path = Path(dir_path, "users.csv")
    doc = open(path, 'rb')
    bot.send_document(chat_id=call.message.chat.id, document=doc)


# send_document


bot.polling(none_stop=True)
