from loader import postgres_user_group, redman_user_group

from exceptions.db_exceptions import NoSchedule, EmptyKey

TABLE_NAME = "user_group"

def create_link_in_postgres(user_id: int, group: int) -> None:
    try:
        data = postgres_user_group.select(
            table_name=TABLE_NAME, 
            conditions={"user_id": user_id})
    except NoSchedule:
        data = [user_id, group]
        postgres_user_group.insert_into(
            table_name=TABLE_NAME, 
            values=data)
    else:
        if data[0][0] == user_id:
            return

        postgres_user_group.update(
            table_name=TABLE_NAME, 
            data={"group_number": group}, 
            conditions={"user_id": user_id})


def create_link_in_redis(key: int, value: int) -> None:
    redman_user_group.set_value(str(key), str(value))


def get_from_postgres(user_id: int) -> int:
    try:
        group = postgres_user_group.select(
            table_name=TABLE_NAME, 
            conditions={"user_id": user_id},
            columns=["group_number"])
    except NoSchedule:
        raise
    else:
        return group[0][0]


def get_from_redis(user_id: int) -> int:
    try:
        group = redman_user_group.get_value(key=str(user_id))
    except EmptyKey:
        raise
    else:
        return group

def create_user_group_link(user_id: int, group: int) -> None:
    create_link_in_postgres(user_id=user_id, group=group)
    create_link_in_redis(key=user_id, value=group)


def get_user_group_link(user_id: int) -> int:
    try:
        group = get_from_redis(user_id=user_id)
    except EmptyKey:
        group = get_from_postgres(user_id=user_id)
    except NoSchedule:
        raise

    return group