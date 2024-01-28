from aiogram import Dispatcher, Bot, types
from dotenv import load_dotenv, find_dotenv
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv(find_dotenv())

telegram_token = os.getenv("TELEGRAM_TOKEN")

storage = MemoryStorage()

bot = Bot(token=telegram_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)