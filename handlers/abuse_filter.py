import json
import string
from aiogram import types
from aiogram.dispatcher import Dispatcher


async def abuse_filter(message: types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split()} \
            .intersection(set(json.load(open('obscene_words.json')))) != set():
        await message.answer(text=f'{message.from_user.first_name} {message.from_user.last_name},'
                                  f' мат и оскорбления запрещены! Сообщение удалено!')
        await message.delete()


def register_handlers_abuse_filter(dp: Dispatcher):
    dp.register_message_handler(abuse_filter)
