from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    ReplyKeyboardMarkup
    )


confirm_completely_update = KeyboardButton(text="Да, обновить всё расписание")
deny_completely_update = KeyboardButton(text="Нет, я передумал")

def completely_update_markup():
    builder = ReplyKeyboardBuilder()
    builder.add(confirm_completely_update)
    builder.add(deny_completely_update)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

