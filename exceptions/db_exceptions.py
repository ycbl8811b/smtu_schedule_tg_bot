from utils.translator import translated_day

class CustomError(Exception):
    pass


class TableNotFound(CustomError):
    def __init__(self, table_name):
        self.table_name = table_name
        self.message = f"Таблица {table_name} не сущесвует"
        super().__init__(self.message)



class NoSchedule(CustomError):
    def __init__(self):
        self.message = "Простите, но расписания с заданными параметрами не существует!\n" + \
                        "Вы уверены, что введённые критерии верны?"
        super().__init__(self.message)



class EmptyKey(CustomError):
    def __init__(self, key, db):
        self.key = key
        self.db = db
        self.message = f"Ключ {key} в Redis-database[{db}] пуст. Удаление ключа..."
        super().__init__(self.message)



class DayNotInSchedule(CustomError):
    def __init__(self, day, group):
        self.day = day
        self.group = group
        self.message = f"У группы {group} нет пар {translated_day(day)}"
        super().__init__(self.message)