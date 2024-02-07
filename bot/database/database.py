import pymysql
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

host = os.getenv("HOST")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
db_name = os.getenv("DB_NAME")


async def create_tables_if_not_exists():
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("БД успешно подключена")

        with connection.cursor() as cursor:
            create_table_chatbot_data = '''
            CREATE TABLE IF NOT EXISTS chatbot_data (
                username VARCHAR(255),
                question TEXT,
                answer TEXT,
                tokens INT
            )
            '''
            create_table_users_info = '''
            CREATE TABLE IF NOT EXISTS users_info (
                id INTEGER AUTO_INCREMENT PRIMARY KEY,
                tg_user_id INTEGER,
                balance FLOAT
            )
            '''
            cursor.execute(create_table_chatbot_data)
            cursor.execute(create_table_users_info)

        connection.commit()

    except Exception as ex:
        print("Не удалось установить соединение с БД или добавить данные")
        print(ex)
    finally:
        if connection:
            connection.close()


# Первоначальная регистрация
async def create_user_info(user_id):
    connection = None
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("БД успешно подключена")

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users_info WHERE tg_user_id = %s", (user_id,))
            user_tg = cursor.fetchone()

        if not user_tg:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users_info (tg_user_id, balance) VALUES (%s, 0)", (user_id,))
            connection.commit()
            print("Первоначальная регистрация записалась в бд")

    except Exception as ex:
        print("Не удалось установить соединение с БД")
        print(ex)

    finally:
        if connection:
            connection.close()


async def insert_chatlog(username_tg, question_tg, answer_tg, tokens):
    connection = None
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("БД успешно подключена")


        with connection.cursor() as cursor:
            sql = "INSERT INTO chatbot_data (username, question, answer, tokens) VALUES (%s, %s, %s, %s)"
            values = (username_tg, question_tg, answer_tg, tokens)
            cursor.execute(sql, values)
            connection.commit()
            print("Данные успешно добавлены в базу")

    except Exception as ex:
        print("Не удалось установить соединение с БД или добавить данные")
        print(ex)

    finally:
        if connection:
            connection.close()


