from aiogram import Bot
from aiogram.enums import ParseMode
import asyncio, os

from Modules.dispatcher import dp

async def main() -> None:
    bot = Bot(os.getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
