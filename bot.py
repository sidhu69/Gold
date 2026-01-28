import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, BOT_DEFAULTS
import handlers_start
import handlers_main
import handlers_buy

bot = Bot(token=TOKEN, default=BOT_DEFAULTS)
dp = Dispatcher(storage=MemoryStorage())

handlers_start.register(dp, bot)
handlers_main.register(dp, bot)
handlers_buy.register(dp, bot)

async def main():
    print("Bot running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
