from typing import Union, List

import asyncio
from aiogram.filters import BaseFilter
from aiogram.types import Message

from utils.check_type import is_list_elems_type

class KeyboardFilter(BaseFilter):
    def __init__(self, required_data: Union[List[str], str]):
        if isinstance(required_data, str):
            self.required_data = required_data.lower()

        elif isinstance(required_data, list) and is_list_elems_type(required_data, str):
            self.required_data = list(map(str.lower, required_data))
        else:
            raise ValueError(f"required_data must be str or List[str], not {type(required_data)}!")

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.required_data, list):
            return message.text.lower() in self.required_data
        else:
            return message.text.lower() == self.required_data

