from typing import Union

from utils.check_type import is_digit

weeks = {
    "верхняя": "Верхняя неделя",
    "нижняя": "Нижняя неделя",
    "обе": "Обе недели",
    "обе недели": "Обе недели"
}

days = {
    "пн": "Понедельник",
    "вт": "Вторник",
    "ср": "Среда",
    "чт": "Четверг",
    "пт": "Пятница",
    "сб": "Суббота"
}


def validated_group(group: str) -> int:
    if is_digit(group):
        return int(group)
    return None


def validated_week(week: str) -> Union[str, None]:
    return weeks.get(week.lower(), None)


def validated_day(day: str) -> str:
    if day.lower() in days.keys():
        return days.get(day.lower(), None)
    return day.capitalize()