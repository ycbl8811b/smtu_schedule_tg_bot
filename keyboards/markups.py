from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    ReplyKeyboardMarkup
    )

group = InlineKeyboardButton(text="Группа", callback_data="group_number")
week = InlineKeyboardButton(text="Неделя", callback_data="week")
day = InlineKeyboardButton(text="День", callback_data="day")
teacher = InlineKeyboardButton(text="ФИО преподавателя", callback_data="name")


add_criteria = KeyboardButton(text="➕ Добавить/изменить критерий")
confirm = KeyboardButton(text="✅ Применить фильтр")

week_up = KeyboardButton(text="Верхняя")
week_down = KeyboardButton(text="Нижняя")
week_both = KeyboardButton(text="Обе недели")

days = [KeyboardButton(text="пн"), KeyboardButton(text="вт"), KeyboardButton(text="ср"), KeyboardButton(text="чт"), KeyboardButton(text="пт"), KeyboardButton(text="сб")]

schedule_request = KeyboardButton(text="❗️ Запросить обновление расписания")
schedule_request_confirm = KeyboardButton(text="Да, критерии указаны верно")
schedule_request_cancel = KeyboardButton(text="Нет, изменить критерии")

cancel = KeyboardButton(text="❌ Отмена")

def filter_markup() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.max_width = 1
    
    builder.add(group)
    builder.add(week)
    builder.add(day)
    # builder.add(teacher)

    return builder.as_markup()


def confirm_filter_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(add_criteria)
    builder.add(confirm)
    builder.add(cancel)

    builder.adjust(2, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def week_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(week_up)
    builder.add(week_down)
    builder.add(week_both)
    builder.add(cancel)

    builder.adjust(2, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def days_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for day in days:
        builder.add(day)
    builder.add(cancel)

    builder.adjust(6, 1)
    return builder.as_markup(resize_keyboard=True)

def cancel_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(cancel)

    return builder.as_markup(resize_keyboard=True)


def schedule_request_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(schedule_request)

    return builder.as_markup(resize_keyboard=True)


def approve_schedule_request_markup() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(schedule_request_confirm)
    builder.add(schedule_request_cancel)

    return builder.as_markup(resize_keyboard=True)