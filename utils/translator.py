from typing import Union

from utils.validation.bot_validation import days

keys = {
    "group_number": "Группа",
    "week": "Неделя",
    "day": "День",
    "teacher": "Преподаватель"
}

days = {
    "Понедельник": "в понедельник",
    "Вторник": "во вторник",
    "Среда": "в среду",
    "Четверг": "в четверг",
    "Пятница": "в пятницу",
    "Суббота": "в субботу"
}

def translated_key(key: str) -> str:
    return keys[key]

def translated_value(value: Union[str, int]) -> Union[str, int]:
    if isinstance(value, int):
        return value
    if value in days.values():
        return value.capitalize()


def translated_day(day: str) -> str:
    return days[day]