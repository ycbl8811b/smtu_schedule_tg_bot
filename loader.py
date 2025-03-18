from aiogram import Bot, Dispatcher
from ntplib import NTPClient

from utils.web.parser import Parser
from utils.render.table_manager import TableManager

from db.postgre_manager import PostgreManager
from db.redis_manager import RedisManager

from assets.bot_config import api_key, website_url

parser = Parser(url=website_url)
postgres_schedule = PostgreManager("schedule_bot", "127.0.0.1", "postgres", "postgres", "5432")
postgres_user_group = PostgreManager("user_group_link", "127.0.0.1", "postgres", "postgres", "5433")
redman_schedule = RedisManager(host="127.0.0.1", db="0")
redman_user_group = RedisManager(host="127.0.0.1", db="1")
tableman = TableManager()
ntpclient = NTPClient()
bot = Bot(token=api_key)
dp = Dispatcher()