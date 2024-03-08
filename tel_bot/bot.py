import os
import sqlite3
import sys
import time

import telebot
from config import BOT_TOKEN, hashtag, channels_id, URL
from db import create_db, clean_bd
from parser.parser import parse_website

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Бот запущен.')
    while True:
        publish_to_channel()


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.reply_to(message, 'Бот отключен.')
    bot.stop_bot()


@bot.message_handler(commands=['clean_bd'])
def clean(message):
    clean_bd()
    bot.reply_to(message, 'База данных очищена')


@bot.message_handler(commands=['post'])
def post(message):
    bot.reply_to(message, 'Парсинг начался...')
    for url in URL:
        parse_website(url=url)
    bot.reply_to(message, 'Выполнен парсинг')


@bot.message_handler(commands=['restart'])
def restart(message):
    bot.reply_to(message, 'Перезагрузка бота...')
    time.sleep(1)
    bot.stop_polling()
    os.system(f'python "{sys.argv[0]}" &')
    sys.exit()


def publish_to_channel():
    try:
        connection = sqlite3.connect('articles.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM articles WHERE published = 0")
        existing_article = cursor.fetchall()
        for article in existing_article:
            if article:
                if hashtag != "off":
                    publish_text = f"{article[1]}\n\n{article[2]}\n\n{article[3]}"
                else:
                    publish_text = f"{article[1]}\n\n{article[3]}"
                bot.send_message(chat_id=channels_id, text=publish_text)
                cursor.execute("UPDATE articles SET published = 1 WHERE article_title = ?", (article[1],))
                connection.commit()
                time.sleep(10)
        cursor.close()
        connection.close()
        time.sleep(10)
    except Exception as ex:
        print(ex)




create_db()
bot.polling(none_stop=True, interval=0)
