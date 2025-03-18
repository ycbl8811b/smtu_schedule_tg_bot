import asyncio
import logging

from loader import bot, dp

from handlers.user.common import user_common_router
from handlers.user.get_schedule import schedule_router
from handlers.user.request_schedule import request_router

from utils.date import handle_week

logging.basicConfig(level=logging.INFO)

async def main():
    handle_week()
    dp.include_router(user_common_router)
    dp.include_router(schedule_router)
    dp.include_router(request_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    