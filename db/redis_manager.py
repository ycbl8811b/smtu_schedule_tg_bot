from redis import Redis
from typing import Union

from exceptions.db_exceptions import EmptyKey

class RedisManager:
    def __init__(self, host="127.0.0.1", port=6379, db=0):
        self.__host = host
        self.__port = port
        self.__db = db

        self.__connect()

    def __connect(self) -> None:
        try:
            r = Redis(host=self.__host, port=self.__port, db=self.__db)
            print(f"Connected to redis-database[{self.__db}] successfuly!")
        except ValueError:
            raise
        else:
            self.__r = r


    def set_value(self, key: str, value: str) -> None:
        self.__r.set(key, value)


    def get_value(self, key) -> Union[str, int]:
        value = self.__r.get(key)
        if value is None or value == b'[]':
            raise EmptyKey(key, self.__db)

        if isinstance(value, bytes):
            return value.decode("utf-8")

        if isinstance(value, int):
            return value


    def delete_data(self, key) -> None:
        self.__r.delete(key)