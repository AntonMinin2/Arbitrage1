import asyncio
from aiogram import Bot, Dispatcher
from telethon import TelegramClient

from app.handlers import router




# Запуск процесса поллинга новых апдейтов
async def main():

    bot = Bot(token="7291861554:AAG2Pi9wIneFwAJTbjkfwc9XTqhgYLAocAY")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
