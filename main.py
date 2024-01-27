import logging
from aiogram import Bot, Dispatcher, types
from bot import dp, bot
from dotenv import load_dotenv, find_dotenv
import os
from fastapi import FastAPI

load_dotenv(find_dotenv())

telegram_token = os.getenv("TELEGRAM_TOKEN")
ngrok_url = os.getenv("NGROK_URL")
admin_id = os.getenv("ADMIN_ID")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
WEBHOOK_PATH = f"/bot/{telegram_token}"
WEBHOOK_URL = f"{ngrok_url}{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    await bot.send_message(chat_id=admin_id, text='Бот запущен')
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.send_message(chat_id=admin_id, text='Бот выключен')
    await bot.session.close()
