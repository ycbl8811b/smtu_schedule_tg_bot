import asyncio
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.markups import confirm_filter_markup
from utils.translator import translated_key, translated_value
from utils.user_data import get_user_group_link

def generate_message(data: dict) -> str:
    msg = ""
    for key, value in data.items():
        msg += f"{translated_key(key)}: {value}\n"
    return msg


def check_query_completeness(message: Message, query: dict):
    def check_group():
        nonlocal query
        if not "group_number" in query:
            try:
                group = get_user_group_link(user_id=message.from_user.id)
            except NoSchedule:
                raise
            else:
                query["group_number"] = int(group)
    check_group()


async def check_filter_completeness(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if len(data.keys()) == 3:
        await message.answer(
            "Вы хотите получить расписание со следующими критериями:",
            reply_markup=confirm_filter_markup())
        await message.answer(generate_message(data))
    else:
        await message.answer(
            generate_message(data))

        await message.answer(
            "Хотите ли добавить/изменить критерий?",
            reply_markup=confirm_filter_markup())