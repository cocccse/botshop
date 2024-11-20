from aiogram import F, types, Router, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.web_app_info import WebAppInfo
import os

from database.orm import (orm_get_categories,
                                orm_get_items,
                                orm_add_user,
                                orm_get_user,
                                orm_get_product_by_category_and_item,
                                orm_get_category_by_id,
                                orm_get_item_by_id)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from keyboards.inline import get_callback_btns, get_url_btns
from keyboards.reply import get_keyboard

user_rt = Router()

kbStart = get_keyboard(
            "📦 Товар",
            "📌 О нас",
            "🧑🏻‍💻 Профиль",

            placeholder="Выберите пункт меню",
            sizes=(2, 1)
        )

kbProduct = get_keyboard(
            "Обувь",
            "Одежда",
            "🕹 Главное меню",
            placeholder="Выберите категорию товаров",
            web_apps={0: 'https://cocccse.github.io', 1: 'https://habr.com/ru/articles/666278/'},
            sizes=(2, 1)
        )

@user_rt.message(CommandStart())
async def start(message):
    await message.answer('Здравствуй новый пользователь', reply_markup=kbStart)

@user_rt.message(F.text == '📌 О нас')
async def info(message):
    await message.anwer('📍 г.Бендеры, ул.Дружбы 111Б\n'
                        '📞 +37377700011')

@user_rt.message(StateFilter('*'),F.text == '🧑🏻‍💻 Профиль')
async def profil(message, FSMContext, AsyncSession):
    await state.set_state(Info.profil)
    user = await orm_get_user(session, message.from_user.id)
    if user.last_name is None:
        await message.answer(f"🔻 <b>{user.first_name}</b>\n"
                             f"Il tuo ID: {user.user_id}\n"
                            f"Bilancia 💶: {user.balance}€\n",
                            parse_mode=ParseMode.HTML,reply_markup=reply.start_kb.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder='Seleziona la voce del menu...'))
    else:
        await message.answer(f"🔻 <b>{user.first_name} {user.last_name}</b>\n"
                             f"Il tuo ID: {user.user_id}\n"
                             f"Bilancia 💶: {user.balance}€\n",
                             parse_mode=ParseMode.HTML, reply_markup=reply.start_kb.as_markup(
                resize_keyboard=True,
                input_field_placeholder='Seleziona la voce del menu...'))
    await state.clear()

@user_rt.message(F.text == '📦 Товар')
async def profil(message):
    await message.answer('Выберите категорию товаров', reply_markup=kbProduct)

