# import pymysql
# from dotenv import load_dotenv, find_dotenv
# import os
#
# load_dotenv(find_dotenv())
#
# host = os.getenv("HOST")
# user = os.getenv("USER")
# password = os.getenv("PASSWORD")
# db_name = os.getenv("DB_NAME")
#
# try:
#     connection = pymysql.connect(
#         host=host,
#         port=3306,
#         user=user,
#         password=password,
#         database=db_name,
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print("successfully connected...")
#     print("#" * 20)
#
# except Exception as ex:
#     print("Connection refused...")
#     print(ex)

import sqlite3 as sq

db = sq.connect('bot/database/database_users_info.db')
cur = db.cursor()


def create_db():
    cur.execute('''CREATE TABLE IF NOT EXISTS chatbot_data
                  (username TEXT, question TEXT, answer TEXT)''')

    cur.execute("CREATE TABLE IF NOT EXISTS users_info("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_user_id INTEGER,"
                "balance REAL)")
    db.commit()


# Первоначальная регистрация
async def create_user_info(user_id):
    user = cur.execute("SELECT * FROM users_info WHERE tg_user_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users_info (tg_user_id, balance) VALUES ({key}, 0)".format(key=user_id))
        db.commit()


# Логирование ответ-вопрос
async def insert_chatlog(username_tg, question_tg, answer_tg):
    sql = "INSERT INTO chatbot_data (username, question, answer) VALUES (?, ?, ?)"
    values = (username_tg, question_tg, answer_tg)
    cur.execute(sql, values)
    db.commit()