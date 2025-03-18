from loader import dp
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from states import Filter
from keyboards.admin_markups import completely_update_markup
from utils.check_access import is_admin
from loader import parser
admin_common_router = Router()


@admin_common_router.message(default_state, Command("update_schedule"))
async def update_all_schedule(message: Message, command: CommandObject) -> None:
    if not is_admin(user_id=message.from_user.id):
        return
    
    if command.args is None:
        await message.answer(
            text="Вы уверены, что хотите обновить всё расписание для всех групп?",
            reply_markup=completely_update_markup()
        )
        return
    

    try:
        args = command.args.split(" ")
    except ValueError:
        await message.answer(
            "Ошибка: неправильный ввод команды. Правильный формат:\n"
            "/update_schedule <group>")
        return
    else:
        group = args[0]
        parser.set_group(group)
        parser.parse_schedule()

