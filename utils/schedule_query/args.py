from utils.validation.bot_validation import validated_group
from utils.check_type import is_digit

from utils.validation.bot_validation import (
    weeks, days, 
    validated_day, validated_group, validated_week
)

def handle_args(args: list) -> dict:
    query = {}
    for arg in args:
        if is_digit(arg):
            query["group_number"] = validated_group(arg)
        elif arg in weeks:
            query["week"] = validated_week(arg)
        elif arg in days:
            query["day"] = validated_day(arg)
    return query