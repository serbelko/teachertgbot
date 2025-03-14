import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from dotenv import load_dotenv

dp = Dispatcher()

@dp.message(CommandStart())
async def echo(message: Message) -> None:
    await message.answer("Привет")


async def main() -> None:
    # переименуй файл .env.dist в .env и подставь соотвествующие данные
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    
    dp.message.register(echo, F.text)

    bot = Bot(token=bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
