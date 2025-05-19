import asyncio
from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from database.db import init_db
from app.handlers.start import router

async def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)


    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down")