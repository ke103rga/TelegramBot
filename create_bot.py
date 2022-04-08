from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

token = "5183698640:AAHW-dOwx_CrQbifZO4CytogG0q6v0xNfoY"

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
