import sqlite3 as sq

db = sq.connect('S:/chatgpt_bot/bot/database/database_users_info.db')
cur = db.cursor()


# def create_db():
#     cur.execute("CREATE TABLE IF NOT EXISTS users_info("
#                 "id INTEGER PRIMARY KEY AUTOINCREMENT, "
#                 "tg_user_id INTEGER,"
#                 "balance REAL)")
#     db.commit()

async def create_user_info(user_id):
    user = cur.execute("SELECT * FROM users_info WHERE tg_user_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users_info (tg_user_id) VALUES ({key})".format(key=user_id))
        db.commit()