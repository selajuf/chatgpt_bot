from aiogram import Dispatcher, Bot, types
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

telegram_token = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)