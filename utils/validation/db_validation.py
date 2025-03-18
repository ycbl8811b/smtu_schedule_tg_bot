from typing import Optional
from datetime import time
from utils.date import current_week


def validated_teacher_name(name):
    return name.replace("\t","").replace("\n","")


def validated_img_name(name):
    return name.replace(" ", "_")


def validated_time(time):
    return f"{time.hour:02}:{time.minute:02}"


def validated_sql_condition(conditions: dict, operator: str = ""):
    def user_id_sql_condition():
        user_id = conditions.pop("user_id")
        return f"user_id={user_id} {operator.upper()} "


    def group_sql_condition():
        group_number = conditions.pop("group_number")
        return f"group_number={group_number} {operator.upper()} "


    def week_sql_condition():
        week = conditions.pop("week", current_week())
        if week in ["Нижняя неделя", "Верхняя неделя"]:
            return f"(week='{week}' OR week='Обе недели') {operator.upper()} "
        else:
            return ""

    if "user_id" in conditions:
        condition_query = user_id_sql_condition()
    else:
        condition_query = group_sql_condition() + week_sql_condition()
    
    condition_query = condition_query.removesuffix(f" {operator.upper()} ")
    return condition_query


def validated_sql(data):
    if isinstance(data, str):
        return f"'{data}'"
    return data

def validate_postgres_data(data):
    res = []
    for row_id in range(len(data)):
        row = data[row_id]
        if isinstance(row, tuple) or isinstance(row, list):
            data[row_id] = list(data[row_id])
            row = data[row_id]
            for column_id in range(len(row)):
                value = data[row_id][column_id]
                if isinstance(value, time):
                    data[row_id][column_id] = validated_time(value)
                    

def validated_fetch_columns(columns):
    res = []
    for column in columns:
        res.append(column[0])
    return res