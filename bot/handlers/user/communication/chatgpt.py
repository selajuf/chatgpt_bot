from aiogram import types, Dispatcher
from loader import bot
from aiogram.dispatcher import FSMContext
from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
import os
from bot.states.talk import AI
from bot.database.database import insert_chatlog
import tiktoken

load_dotenv(find_dotenv())

openai_token = os.getenv("OPENAI_TOKEN")
max_symbols_limit = int(os.getenv("MAX_SYMBOLS"))

client = AsyncOpenAI(
    base_url="https://api.mandrillai.tech/v1", # endpoint
    api_key=openai_token
)


async def chat_talk(message: types.Message, state: FSMContext):
    if message.text == '/start':
        await message.answer(
            f'{message.from_user.full_name}, добро пожаловать в бота.\n\nОтправь мне сообщение, а я на него отвечу.')
        return
    data = await state.get_data()
    data = data.get('history')
    response_message = await message.reply("Генерирую ответ...")

    history = []
    if len(data) > 1:
        for index in range(0, len(data)):
            if data[index].get('question') is None:
                data[index]['question'] = message.text
                d = {"role": "user", "content": data[index]['question']}
                history.append(d)
            else:
                d = [{"role": "user", "content": data[index]['question']},
                     {"role": "assistant", "content": data[index].get('answer')}]
                history += d
    else:
        data[0]['question'] = message.text
        d = {"role": "user", "content": data[0].get('question')}
        history.append(d)
    print(f'Запрос от пользователя: {history}')
    if message.text and len(message.text) > max_symbols_limit:
        await bot.edit_message_text(
            f"Превышено ограничение в {max_symbols_limit} символов. Ваш ответ содержит {len(message.text)} символов.",
            chat_id=message.chat.id, message_id=response_message.message_id)
        return

    resp_ai = await generate(history)

    if resp_ai:
        data[-1]['answer'] = resp_ai.replace('\n', '')
        username_tg = f"@{message.from_user.username}"
        question_tg = data[-1]['question']
        answer_tg = data[-1]['answer']
        tokens = await num_tokens_from_string(resp_ai, "cl100k_base")
        print("Кол-во токенов от нейросети:", tokens)
        await insert_chatlog(username_tg, question_tg, answer_tg, tokens)
        data.append({"question": None, "answer": None})
        if len(data) > 10:
            await state.update_data(history=[{"question": None, "answer": None}])
        await state.update_data(history=data)
        await bot.edit_message_text(resp_ai, chat_id=message.chat.id, message_id=response_message.message_id,
                                    parse_mode='MarkDown')
    else:
        error_message = "Произошла ошибка при генерации ответа."
        await bot.edit_message_text(error_message, chat_id=message.chat.id, message_id=response_message.message_id)


async def generate(history) -> str:
    try:
        response = await client.chat.completions.create(
            model="gemini-pro",
            messages=history,
            max_tokens=500
        )
        if response and response.choices:
            return str(response.choices[0].message.content)
        else:
            return None
    except Exception as e:
        print(e)
        return None


async def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(chat_talk, state=AI.talk)