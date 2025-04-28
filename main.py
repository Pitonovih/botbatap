import logging
from aiogram import executor
from bot_instance import dp
from handlers import *
from database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)

async def on_startup(dp):
    init_db()
    logger.info("Бот запущен ✅")

if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        relax=0.5
    )
