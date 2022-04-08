from aiogram.utils import executor
from create_bot import dp
from handlers import ClientPart, AdminPart, CommonPart
from data_base import sqlite_db


async def on_startup(_):
    print("Bot online")
    sqlite_db.sql_start()


ClientPart.register_handler_client(dp)
AdminPart.register_handler_admin(dp)
CommonPart.register_handler_mat(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
