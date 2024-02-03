import logging
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv, find_dotenv
from bot.misc.set_bot_commands import set_default_commands
import os
from loader import dp, bot
from bot.handlers.user.commands import start
from bot.handlers.user.communication import chatgpt
from aiohttp import web

load_dotenv(find_dotenv())

telegram_token = os.getenv("TELEGRAM_TOKEN")
ngrok_url = os.getenv("NGROK_URL")
ADMIN_ID = os.getenv("ADMIN_ID")

Bot.set_current(bot)
Dispatcher.set_current(dp)
app = web.Application()

start.register_handlers_users(dp)
chatgpt.register_handlers_users(dp)

webhook_path = f'{ngrok_url}/{telegram_token}'

async def set_webhook():
    webhook_uri = f'{webhook_path}'
    await bot.set_webhook(
        webhook_uri
    )


async def on_startup(_):
    await set_webhook()
    await set_default_commands(dp)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != webhook_path:
        await bot.set_webhook(url=webhook_path)
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')


async def on_shutdown(_):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот выключен')


async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[
            index + 1:]
    if token == telegram_token:
        update = types.Update(**await request.json())
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)


app.router.add_post(f'/{telegram_token}',
                    handle_webhook)

if __name__ == "__main__":
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('aiogram').setLevel(logging.DEBUG)

    web.run_app(
        app,
        host='0.0.0.0',
        port=8000
    )
