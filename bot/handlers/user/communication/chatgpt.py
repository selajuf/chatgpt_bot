from aiogram import types, Dispatcher
from loader import bot
from aiogram.dispatcher import FSMContext
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
from bot.states.talk import AI

load_dotenv(find_dotenv())

openai_token = os.getenv("OPENAI_TOKEN")

client = OpenAI(
    base_url="https://api.mandrillai.tech/v1", # endpoint
    api_key=openai_token
)


async def chat_talk(message: types.Message, state: FSMContext):
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
                d = [{"role": "user", "content": data[index]['question']}, {"role": "assistant", "content": data[index].get('answer')}]
                history += d
    else:
        data[0]['question'] = message.text
        d = {"role": "user", "content": data[0].get('question')}
        history.append(d)
    print(history)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    print(response.choices[0].message.content)
    resp_ai = response.choices[0].message.content
    data[-1]['answer'] = resp_ai.replace('\n', '')
    text = f"{message.from_user.username}\nQ:{data[-1]['question']}\nA:{data[-1]['answer']}"
    data.append({"question": None, "answer": None})
    if len(data) > 10:
        await state.update_data(history=[{"question": None, "answer": None}])
    await state.update_data(history=data)
    await bot.edit_message_text(resp_ai, chat_id=message.chat.id, message_id=response_message.message_id, parse_mode='MarkDown')

def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(chat_talk, state=AI.talk)