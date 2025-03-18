import asyncio
from aiogram import Router, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile,
    ReplyKeyboardRemove
)

from states import Filter
from keyboards.markups import (
    filter_markup, 
    confirm_filter_markup, 
    week_markup, 
    days_markup,
    schedule_request,
    approve_schedule_request_markup
)

from filters.input_type import InputTypeFilter
from filters.keyboard_btn_data import KeyboardFilter
from assets.filter_config import weeks_names, days_names

from utils.schedule_query.data_check import check_filter_completeness, check_query_completeness
from utils.schedule_manager import get_table_path, save_schedule_to_redis, table_on_tg_server
from utils.validation.bot_validation import validated_group, validated_week, validated_day
from utils.schedule_query.args import handle_args
from utils.user_data import get_user_group_link, create_user_group_link

from exceptions.db_exceptions import DayNotInSchedule, NoSchedule


schedule_router = Router()


@schedule_router.message(Command("schedule"))
async def get_schedule(message: Message, state: FSMContext) -> None:
    try:
        group = get_user_group_link(user_id=message.from_user.id)
    except NoSchedule:
        await message.answer("Простите, но мы не знаем вашу группу.\nПожалуйста, воспользуйтесь командой /filter")
    else:
        await state.set_state(Filter.choosing_group)
        await state.update_data(group_number=group)
        await confirm_filter(message=message, state=state)


@schedule_router.message(Command("filter"))
async def start_filter(message: Message, command: CommandObject, state: FSMContext) -> None:
    if command.args is None:
        await message.answer(
            "Выберите критерий, по которому хотите отфильтровать расписание:",
            reply_markup=filter_markup())
        return
    
    try:
        args = command.args.split(" ")
    except ValueError:
        await message.answer(
            "Ошибка: неправильный ввод команды. Правильный формат:\n"
            "/filter <group> <week> <day> <teacher>")
        return
    else:
        query = handle_args(args)
        try:
            check_query_completeness(message=message, query=query)
        except NoSchedule:
            await message.answer("Вы не указали группу", reply_markup=ReplyKeyboardRemove())
        else:
            await state.update_data(query)
            await confirm_filter(message=message, state=state)

# Этап обработки группы

@schedule_router.callback_query(F.data == "group_number")
async def get_group(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Filter.choosing_group)
    await callback_query.answer()
    await callback_query.message.answer(
        "Пожалуйста, введите номер группы",
        reply_markup=ReplyKeyboardRemove())


@schedule_router.message(InputTypeFilter(input_type=int), Filter.choosing_group)
async def process_group(message: Message, state: FSMContext) -> None:
    group = validated_group(message.text)
    await state.update_data(group_number=group)
    await state.set_state(Filter.confirm_filter)
    await check_filter_completeness(message, state)


@schedule_router.message(InputTypeFilter(input_type=str), Filter.choosing_group)
async def process_group_invalid(message: Message, state: FSMContext) -> None:
    await message.answer("Номер группы должен быть числом!")
    await message.answer(
        "Пожалуйста, введите номер группы",
        reply_markup=ReplyKeyboardRemove())


# Этап обработки недели

@schedule_router.callback_query(F.data == "week")
async def get_week(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Filter.choosing_week)
    await callback_query.answer()
    await callback_query.message.answer(
        "Пожалуйста, выберите неделю:\n\n"
        "_Примечание_: если необходимо получить расписание на *ВСЕ* недели (нижняя, верхняя, обе), то отмените данное действие!\n"
        "В случае выбора варианта 'Обе недели', Вы получите расписание только тех пар, который есть на *обоих* неделях!",
        reply_markup=week_markup(),
        parse_mode=ParseMode.MARKDOWN)


@schedule_router.message(Filter.choosing_week, KeyboardFilter(weeks_names()))
async def process_week(message: Message, state: FSMContext) -> None:
    week = validated_week(message.text)
    await state.update_data(week=week)
    await state.set_state(Filter.confirm_filter)
    await check_filter_completeness(message, state)


@schedule_router.message(Filter.choosing_week)
async def process_week_invalid(message: Message) -> None:
    await message.answer(
        "Такой недели не существует.\n"
        "Пожалуйста, воспользуйтесь кнопками.",
        reply_markup=week_markup())



# Этап обработки дня

@schedule_router.callback_query(F.data == "day")
async def get_day(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Filter.choosing_day)
    await callback_query.answer()
    await callback_query.message.answer(
        "Пожалуйста, выберите название дня на который хотите узнать расписание",
        reply_markup=days_markup())


@schedule_router.message(Filter.choosing_day, KeyboardFilter(days_names()))
async def process_day(message: Message, state: FSMContext) -> None:
    day = validated_day(message.text)
    
    await state.update_data(day=day)
    await state.set_state(Filter.confirm_filter)
    await check_filter_completeness(message, state)


@schedule_router.message(Filter.choosing_day)
async def process_day_invalid(message: Message) -> None:
    await message.answer(
        "Такого дня не существует!\n"
        "Пожалуйста, воспользуйтесь кнопками",
        reply_markup=days_markup())


@schedule_router.message(F.text.lower() == "➕ добавить/изменить критерий")
async def add_criteria(message: Message) -> None:
    await message.answer(text="Продолжим...", reply_markup=ReplyKeyboardRemove())
    await message.answer(
            "Выберите критерий, по которому хотите отфильтровать расписание:",
            reply_markup=filter_markup())



@schedule_router.message(F.text.lower() == "✅ применить фильтр")
async def confirm_filter(message: Message, state: FSMContext) -> None:
    query = await state.get_data()
    print("query: ", query)
    try:
        table_path = get_table_path(query.copy())
        if table_on_tg_server(table_path):
            await message.answer_photo(photo=table_path, reply_markup=ReplyKeyboardRemove())
            return
    except DayNotInSchedule as e:
        await message.answer(e.message, reply_markup=ReplyKeyboardRemove())
        return
    except NoSchedule as e:
        await message.answer(e.message, reply_markup=approve_schedule_request_markup())
        return
    else:
        table = FSInputFile(table_path)
        schedule = await message.answer_photo(photo=table, reply_markup=ReplyKeyboardRemove())
        save_schedule_to_redis(query.copy(), schedule.photo[-1].file_id)
        create_user_group_link(user_id=message.from_user.id, group=query["group_number"])
        await state.clear()