import sqlite3


def init_db():
    conn = sqlite3.connect('captcha.db')
    cur = conn.cursor()

    # Create table users
    cur.execute('''
                CREATE TABLE IF NOT EXISTS users
                (
                    user_id       INTEGER PRIMARY KEY,
                    attempts_left INTEGER DEFAULT 5,
                    is_verified   BOOLEAN DEFAULT 0,
                    ban_until     TIMESTAMP,
                    current_captcha TEXT
                )
                ''')

    conn.commit()
    conn.close()

init_db()