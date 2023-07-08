from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import bot_token


storage = MemoryStorage()
bot = Bot(token=bot_token)
dp = Dispatcher(bot=bot, storage=storage)
