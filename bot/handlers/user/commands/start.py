from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot.database.database import create_user_info
from bot.states.talk import AI


async def start_user(message: types.Message, state: FSMContext):
    await create_user_info(message.from_user.id)
    await message.answer(f'{message.from_user.full_name}, добро пожаловать в бота.\n\nОтправь мне сообщение, а я на него отвечу.')
    await AI.talk.set()
    await state.update_data(history=[{"question": None, "answer": None}])


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(start_user, commands='start')
