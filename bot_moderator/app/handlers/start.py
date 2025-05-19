import asyncio
from datetime import timedelta, datetime

from aiogram import Router, types, F
from aiogram.filters import Command

from app.captcha import generate_captcha
from app.handlers import router
from database.storage import get_user, update_verification
import sqlite3

user_captcha = {}
last_captcha_time = {}

@router.message()
async def handle_first_message(message: types.Message):
    # Получаем пользователя и проверяем его статус верификации / get the user and check his verification status
    user = get_user(message.from_user.id)

    # Если пользователь уже верифицирован, пропускаем капчу / If the user is already verified, skip the captcha
    if user.get('is_verified'):
        return

    # Если не верифицирован - показываем капчу / If not verified - show captcha
    correct_emoji, keyboard = generate_captcha()

    conn = sqlite3.connect('captcha.db')
    cur = conn.cursor()
    cur.execute(
        'UPDATE users SET current_captcha = ? WHERE user_id = ?',
        (correct_emoji, message.from_user.id)
    )
    conn.commit()
    conn.close()

    # Сохраняем верный ответ / Keeping the right answer
    user_captcha[message.from_user.id] = correct_emoji
    user_name = message.from_user.first_name

    bot_message = await message.answer(
        f"🔐{user_name} Run a background check:\n"
        f"Choose a smiley face {correct_emoji}",
        reply_markup=keyboard
    )
    await asyncio.sleep(1) #через сколько секунд удалить сообщение коментатора
    await message.delete() #удаляю сообщение коментатора
    await asyncio.sleep(10) #через сколько удалить капчу
    try:
        await bot_message.delete() #удаляю капчу
    except Exception as ex:
        print(f"Error deleting message / Ошибка при удалении сообщения: {ex}")


@router.callback_query(F.data.startswith('captcha_'))
async def check_captcha(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    selected_emoji = callback.data.split('_')[1]
    correct_emoji = user_captcha.get(user_id)

    if not correct_emoji:
        await callback.answer('❌ The captcha is out of date!', show_alert=True)
        await asyncio.sleep(5)
        await callback.message.delete()
        return

    # Получаем текущего пользователя для проверки статуса верификации
    user = get_user(user_id)


    if user.get('is_verified'):
        return

    remaining_attempts = None

    if selected_emoji == correct_emoji:
        # При успешной капче обновляем статус верификации
        update_verification(user_id, success=True)
        await callback.message.edit_text("✅ Test passed!")
        await asyncio.sleep(5)
        await callback.message.delete()
        remaining_attempts = 5
    else:
        remaining_attempts = update_verification(user_id, success=False)
        await callback.answer(f"❌ Wrong! Attempts left: {remaining_attempts}", show_alert=True)

    if remaining_attempts <= 0:
        try:
            chat_id = callback.message.chat.id #получаю id чата где было отправленно сообщение / get the id of the chat room where the message was sent
            user_id =callback.from_user.id
            until_date = int((datetime.now() + timedelta(hours=24)).timestamp()) #Баню на 24ч / blocking user 24 hours

            await callback.message.bot.ban_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                until_date=until_date,
            )
            await callback.message.edit_text("You're banned for 24 hours!")
        except Exception as e:
            print(f'User ban error: {e}')



