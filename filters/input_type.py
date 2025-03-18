from typing import Union
from string import digits

import asyncio
from aiogram.filters import BaseFilter
from aiogram.types import Message

from utils.check_type import is_digit

class InputTypeFilter(BaseFilter): 
    def __init__(self, input_type: Union[str, int]):
        self.input_type = input_type
    
    async def __call__(self, message: Message) -> bool:
        if isinstance(self.input_type, int):
            return is_digit(message)
        return True