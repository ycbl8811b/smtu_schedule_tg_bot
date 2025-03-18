from utils.validation.bot_validation import weeks
from utils.validation.bot_validation import days

def weeks_names():
    return list(weeks.keys()) + list(weeks.values())

def days_names():
    return list(days.keys()) + list(days.values())