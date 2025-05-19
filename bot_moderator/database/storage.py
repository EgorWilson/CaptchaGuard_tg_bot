import sqlite3
from datetime import datetime, timedelta
from database.db import init_db
init_db()

def get_user(user_id: int) -> dict:
    """Получение или создание записи пользователя с преобразованием в словарь
    Retrieve or create a user record with conversion to a dictionary"""

    conn = sqlite3.connect('captcha.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        'INSERT OR IGNORE INTO users (user_id, attempts_left) VALUES (?, ?)',
        (user_id, 5)  # Указываем начальное количество попыток / Specify the initial number of attempts
    )
    conn.commit()

    # Получаем данные пользователя
    cur.execute(
        'SELECT * FROM users WHERE user_id = ?',
        (user_id,)
    )
    user = dict(cur.fetchone())  # Преобразуем в словарь / Convert to a dictionary
    conn.close()
    return user


def update_verification(user_id: int, success: bool) -> int:
    """Обновляем статус верификации и возвращаем оставшиеся попытки
    Update the verification status and return the remaining attempts"""
    conn = sqlite3.connect('captcha.db')
    cur = conn.cursor()

    if success:
        cur.execute(
            'UPDATE users SET is_verified = 1 WHERE user_id = ?',
            (user_id,)
        )
        remaining_attempts = 5
    else:
        # Уменьшаем количество попыток и получаем новое значение / Reduce the number of attempts and get the new value
        cur.execute(
            'UPDATE users SET attempts_left = attempts_left - 1 '
            'WHERE user_id = ? RETURNING attempts_left',
            (user_id,)
        )
        remaining_attempts = cur.fetchone()[0]

        # Блокируем если попытки закончились / Block if the attempts are over
        if remaining_attempts <= 0:
            cur.execute(
                'UPDATE users SET ban_until = ? WHERE user_id = ?',
                (datetime.now() + timedelta(hours=24), user_id)
            )

    conn.commit()
    conn.close()
    return remaining_attempts