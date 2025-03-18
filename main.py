from datetime import time

from PostgreManager import PostgreManager
from Parser import Parser
from TableManager import TableManager
from RedisManager import RedisManager


def get_template():
    def get_columns():
        return ["Start_time", "End_time", "Week", "Classroom", "Group_number", "Lesson", "Teacher_photo", "Teacher_name"]

    def get_columns_types():
        return ["time", "time", "varchar(14)", "varchar(40)", "smallint", "varchar(70)", "varchar(100)", "varchar(100)"]
    
    columns = get_columns()
    columns_types = get_columns_types()

    template = {}
    for i in range(len(columns)):
        template[columns[i]] = columns_types[i]
    return template


def get_schedule(day):
    try:
        return redman.get_value(day)
    except ValueError as e:
        print(e)
        schedule = postgres.select(day)
        redman.set_value(day, schedule)
        return schedule


# parser = Parser("https://www.smtu.ru/ru/viewschedule/", "20121")
# days = parser.parse_schedule()

postgres = PostgreManager("schedule_bot", "127.0.0.1", "postgres", "postgres", "5432")
tableman = TableManager()
redman = RedisManager(host="127.0.0.1", db="0")

schedule = get_schedule("Суббота")

columns_names = ["Начало", "Конец", "Неделя", "Аудитория", "Группа", "Предмет", "Фото", "Преподаватель"]
tableman.render_table(columns_names, schedule)