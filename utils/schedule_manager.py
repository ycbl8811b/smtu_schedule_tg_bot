from typing import Union

from loader import parser, postgres_schedule, redman_schedule, tableman

from exceptions.db_exceptions import (
    TableNotFound, 
    EmptyKey, 
    DayNotInSchedule,
    NoSchedule
)

from utils.date import today, current_week


def table_on_tg_server(table_path):
    return not '.png' in table_path


def generate_key(query) -> str:
    group = str(query.pop("group_number"))
    week = query.pop("week", current_week())
    day = query.pop("day", today())

    key = '-'.join([group,week,day])

    return key


def save_schedule_to_redis(query, file_id) -> None:
    key = generate_key(query)
    redman_schedule.set_value(key, file_id)


def get_schedule(query: dict) -> Union[str, list]:
    def get_schedule_from_redis(query: dict) -> str:
        key = generate_key(query.copy())
        try:
            return redman_schedule.get_value(key)
        except EmptyKey:
            raise
    

    def get_schedule_from_postgres(query: dict) -> list:
        day = query.pop("day", today())
        print("get-postgres query: ", query)
        try:
            return postgres_schedule.select(table_name=day, conditions=query)
        except NoSchedule:
            raise

    try:
        return get_schedule_from_redis(query)
    except EmptyKey:
        return get_schedule_from_postgres(query)
    except NoSchedule:
        raise


def get_table_path(query: dict) -> str:
    try:
        schedule = get_schedule(query)
    except TableNotFound:
        raise DayNotInSchedule(day, query["group_number"])
    except NoSchedule:
        raise

    if isinstance(schedule, str):
        return schedule

    columns_names = ["Начало", "Конец", "Неделя", "Аудитория", "Группа", "Предмет", "Фото", "Преподаватель"]
    table_path = tableman.render_table(columns_names, schedule)
    return table_path
