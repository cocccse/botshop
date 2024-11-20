from aiogram.filters import Filter
from aiogram import Bot
from aiogram.types import Message

class IsAdmin(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        # Проверка, является ли ID отправителя сообщением в списке администраторов
        return message.from_user.id in bot.my_admins_list