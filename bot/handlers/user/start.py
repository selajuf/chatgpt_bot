from aiogram import types, Dispatcher
from bot.database.database import create_user_info


async def start_user(message: types.Message):
    await create_user_info(message.from_user.id)
    await message.answer(f'{message.from_user.full_name}, добро пожаловать в бота.')


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(start_user, commands='start')
