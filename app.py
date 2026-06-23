import asyncio

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor
from aiogram.types import ParseMode

from config import *
from database import initialize_database




bot = Bot(
    token=bot_token,
    parse_mode=ParseMode.HTML
)

storage = MemoryStorage()
dp = Dispatcher(
    bot,
    storage=storage
)



async def on_startup(dispatcher):
    await initialize_database()
    asyncio.create_task(manage_active_giveaways())




if __name__ == '__main__':
    from handlers import dp, manage_active_giveaways


    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
