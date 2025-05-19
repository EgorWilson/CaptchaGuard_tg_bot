import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

EMOJI_SET=['😀', '😎', '🤖', '👻', '🐉', '🦄', '🍕', '🎮', '🚀', '🌈']

def generate_captcha() -> tuple[str, InlineKeyboardMarkup]:
    """генерирую капчу / captcha generation"""
    correct_emoji = random.choice(EMOJI_SET)
    wrong_emojis = random.sample([e for e in EMOJI_SET if e != correct_emoji], 3)

    buttons = [correct_emoji] + wrong_emojis
    random.shuffle(buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=emoji, callback_data=f'captcha_{emoji}')
        for emoji in buttons
    ]])

    return correct_emoji, keyboard

