from loader import dp
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from states import Filter
from utils.schedule_query.data_check import check_filter_completeness

user_common_router = Router()

greet_message = """
    Для получения расписания воспользуйтесь командой:
    /filter <group> <day> <week> <teacher_name>
    
    group - группа (1234). По умолчанию: последняя указанная (нет, если раньше не пользовались)
    day - день (Понедельник/пн). По умолчанию: сегодня
    week - неделя (Нижняя/Верхняя/обе) По умолчанию: все


    Пример:
    /filter 1234 - выводит расписание группы 1234 на сегодня по всем неделям

    /filter 1234 вт нижняя - выводит расписание группы 1234 на вторник по нижней неделе
"""

@user_common_router.message(Command("start"))
async def send_welcome(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(greet_message)


@user_common_router.message(default_state, Command("cancel"))
@user_common_router.message(default_state, F.text.lower() == "❌ отмена")
async def cancel_filter_no_state(message: Message, state: FSMContext) -> None:
    await state.set_data({})
    await message.answer(
        "Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )

@user_common_router.message(Filter.confirm_filter, Command("cancel"))
@user_common_router.message(Filter.confirm_filter, F.text.lower() == "❌ отмена")
async def cancel_invalid_filter(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Фильтры отменены",
        reply_markup=ReplyKeyboardRemove()
    )

@user_common_router.message(Command("cancel"))
@user_common_router.message(F.text.lower() == "❌ отмена")
async def cancel_filter(message: Message, state: FSMContext) -> None:
    await state.set_state(Filter.waiting)
    await message.answer(
        "Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
    await check_completeness(message, state)


@user_common_router.message(Command("sos"))
async def handle_appeal(message: Message, command: CommandObject) -> None:
    pass