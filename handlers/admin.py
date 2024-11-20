from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from filters.chat_types import IsAdmin
from database.orm import (orm_add_product,
                                orm_get_categories,
                                orm_get_items,
                                orm_get_user,
                                )

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard


admin_rt = Router()
admin_rt.message.filter(IsAdmin())

@admin_rt.message(Command('admin'))
async def admin(message):
    await message.answer('qwqw')