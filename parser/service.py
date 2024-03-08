from selenium.webdriver.common.by import By

from config import hashtag, text_length, under_text, proxy

import sqlite3

websites = ["https://forklog.com/tag/uniswap",
            "https://forklog.com/tag/ethereum",
            "https://forklog.com/tag/bitcoin"]


def text_editing(article_title, tags, text_article, parent_element):
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()
    count_symbol = len(article_title) + len(tags)
    all_text = ''
    for p in text_article:
        if p.find_element(By.XPATH, "..") == parent_element:
            if count_symbol + len(p.text) + len(all_text) < text_length:
                all_text += "\n" + p.text
            else:
                all_text += ".."
                all_text += f"\n{under_text}"
                break

    if hashtag == "on":
        rez = {"article_title": article_title,
               "tags": tags,
               "text": all_text}
    else:
        rez = {"article_title": article_title,
               "text": all_text}
    cursor.execute('SELECT * FROM articles WHERE article_title = ?', (rez['article_title'],))
    existing_article = cursor.fetchone()
    if not existing_article:
        cursor.execute('''
            INSERT INTO articles (article_title, tags, text)
            VALUES (?, ?, ?)
        ''', (rez['article_title'], rez.get('tags'), rez['text']))
        connection.commit()
    else:
        pass
