import sqlite3


def create_db():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            article_title TEXT,
            tags TEXT,
            text TEXT,
            published BOOLEAN DEFAULT 0
        )
    ''')


def clean_bd():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM articles")
    connection.commit()
