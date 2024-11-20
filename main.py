import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import WebAppInfo
from aiogram.client.bot import DefaultBotProperties
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession

from database.engine import create_db, drop_db, session_maker

from handlers.user import user_rt
from handlers.admin import admin_rt


ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
ADMIN_ID = os.getenv('ADMIN_ID')
bot.my_admins_list = [int(admin_id) for admin_id in ADMIN_ID.split(',')]

dp = Dispatcher()

dp.include_router(user_rt)
dp.include_router(admin_rt)


async def on_startup(bot):
    # await drop_db()
    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())