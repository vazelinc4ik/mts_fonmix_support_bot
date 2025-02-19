import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core import settings
from middlewares import AlbumMiddleware
from handlers import router


async def main():
    
    bot = Bot(token=settings.BOT.BOT_TOKEN)

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(AlbumMiddleware())
    dp.include_router(router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())