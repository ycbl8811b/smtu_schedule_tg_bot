import asyncio
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from states import Filter
from keyboards.markups import filter_markup, confirm_filter_markup
from utils.schedule_query.data_check import check_filter_completeness

request_router = Router()

@request_router.message(F.text.lower() == "❗️ запросить обновление расписания")
async def requets_schedule(message: Message, state: FSMContext) -> None:
    await message.answer("Спасибо за обращение!")


@request_router.message(F.text.lower() == "да, критерии указаны верно")
async def confirm_request(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Должно быть ошибка в работе сервиса.\n"
        "Благодарим Вас за обратную связь. Мы постараемся как можно скорее исправить проблему!",
        reply_markup=ReplyKeyboardRemove())
    await state.clear()
    pass


@request_router.message(F.text.lower() == "нет, изменить критерии")
async def cancel_request(message: Message, state: FSMContext) -> None:
    await state.set_state(Filter.confirm_filter)
    await check_completeness(message, state)
