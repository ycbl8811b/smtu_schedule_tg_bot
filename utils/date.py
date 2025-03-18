import locale
from datetime import datetime, timedelta
from time import sleep
import threading

# from loader import ntpclient
from ntplib import NTPException, NTPClient

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

ntpclient = NTPClient()

NTP_HOST = "time.google.com"
current_week = "Нижняя неделя"


def current_week():
    return current_week


def handle_week():
    global current_week
    if current_week == "Верхняя неделя":
        current_week = "Нижняя неделя"
    else:
        current_week = "Верхняя неделя"

    threading.Timer(get_seconds_until_next_monday(), handle_week).start()


def to_midnight(curtime):
    return curtime.replace(hour=0, minute=0, second=0, microsecond=0)


def get_seconds_until_next_monday():
    today = get_current_time()
    days_until_end = 7 - today.weekday()
    end_of_week = to_midnight(today + timedelta(days=days_until_end))
    seconds_until_end_of_week =  end_of_week.timestamp() - today.timestamp()
    return seconds_until_end_of_week


def get_current_time():
    try:
        response = ntpclient.request(host=NTP_HOST, version=3)
    except NTPException:
        raise ValueError(f"No response received from {NTP_HOST}")
    else:
        timestamp = response.tx_time
        dt = datetime.fromtimestamp(timestamp)
        return dt


def today():
    curtime = get_current_time()
    return curtime.strftime("%A")
        