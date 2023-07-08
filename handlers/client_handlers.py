from aiogram import Dispatcher, types
from tg_bot import bot
from config import bot_url, greeting, work_hours, location, contacts
from keyboards import kb_client
from data_base import sqlite_db


# @dp.message_handler(commands=('start', 'help'))
async def cmd_start(message: types.Message):
    try:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'{message.from_user.first_name}, {greeting}',
                               reply_markup=kb_client)
        await message.delete()
    except Exception as exc:
        await message.reply(f'Ошибка: {exc}\nНеобходимо запустить бота {bot_url} для того, чтобы он мог Вам написать')


# @dp.message_handler(commands='график')
async def cmd_schedule(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=work_hours)


# @dp.message_handler(commands='расположение')
async def cmd_location(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=location)


# @dp.message_handler(commands='контакты')
async def cmd_contacts(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=contacts)


# @dp.message_handler(commands='меню')
async def cmd_menu(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(callback=cmd_start, commands=('start', 'help'))
    dp.register_message_handler(callback=cmd_schedule, commands='график')
    dp.register_message_handler(callback=cmd_location, commands='расположение')
    dp.register_message_handler(callback=cmd_contacts, commands='контакты')
    dp.register_message_handler(callback=cmd_menu, commands='меню')
