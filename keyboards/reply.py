from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo

def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        web_apps: dict[int, str] = None,  # Словарь с индексами кнопок WebApp и их URL
        sizes: tuple[int] = (2,),
):
    '''
    Пример: - !Индексы отсчет с 0!
    переменная - kbStart = get_keyboard(
            "Веб приложение 1",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Веб приложение 2",
            placeholder="Что вас интересует?",
            request_contact=4,
            request_location=3,
            web_apps={0: 'https://github.com', 4: 'https://example.com'},
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()
    web_apps = web_apps or {}  # Инициализация словаря для WebApp кнопок

    for index, text in enumerate(btns):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        elif index in web_apps:  # Проверка на наличие WebApp кнопки в указанном индексе
            keyboard.add(KeyboardButton(text=text, web_app=WebAppInfo(url=web_apps[index])))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)