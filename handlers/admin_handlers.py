from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base import sqlite_db
from keyboards import kb_admin
from tg_bot import bot
from config import admin_id


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Активировать панель администратора:
# @dp.message_handler(commands='admin')
async def cmd_admin(message: types.Message):
    if message.from_user.id == admin_id:
        await bot.send_message(chat_id=message.from_user.id, text='Панель администратора активирована:',
                               reply_markup=kb_admin)
        await message.delete()


# Начало диалога, загрузка нового пункта меню:
# @dp.message_handler(commands='загрузить', state=None)
async def cmd_start_loading(message: types.Message):
    if message.from_user.id == admin_id:
        await FSMAdmin.photo.set()
        await message.reply(text='Загрузите фото:')


# Выход из состояний (для отмены действий):
# @dp.message_handler(state='*', commands='отменить')  # state="*" - любое состояние бота, в каком бы он не находился
async def cmd_cancel(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply(text='Загрузка отменена.')


# Записываем в словарь первый ответ:
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def cmd_add_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply(text=f'Фото добавлено.\nID изображения в БД:\n{message.photo[0].file_id}')
        await message.answer(text='Введите название:')


# Записываем в словарь второй ответ про название:
# @dp.message_handler(state=FSMAdmin.name)
async def cmd_add_name(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply(text=f'Название "{message.text}" добавлено в БД.')
        await message.answer(text='Введите описание:')


# Записываем в словарь третий ответ с описанием:
# @dp.message_handler(state=FSMAdmin.description)
async def cmd_add_description(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply(text='Описание добавлено в БД.')
        await message.answer(text='Укажите цену:')


# Записываем последний ответ в словарь и используем полученные данные:
# @dp.message_handler(state=FSMAdmin.price)
async def cmd_add_price(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sqlite_db.sql_add_item(state)
        await message.reply(text='Загрузка позиции в БД завершена.')
        await state.finish()


# Удалить запись из базы данных:
# @dp.message_handler(commands='удалить')
async def cmd_delete_item(message: types.Message):
    if message.from_user.id == admin_id:
        read = await sqlite_db.sql_read2()
        for ret in read:
            del_button = InlineKeyboardMarkup()
            del_button.add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}'))
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n\nОписание: {ret[2]}\nЦена: {ret[3]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=del_button)


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_item(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(callback=cmd_admin, commands='admin')
    dp.register_message_handler(callback=cmd_start_loading, commands='загрузить', state=None)
    dp.register_message_handler(callback=cmd_cancel, state='*', commands='отменить')
    dp.register_message_handler(callback=cmd_add_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(callback=cmd_add_name, state=FSMAdmin.name)
    dp.register_message_handler(callback=cmd_add_description, state=FSMAdmin.description)
    dp.register_message_handler(callback=cmd_add_price, state=FSMAdmin.price)
    dp.register_message_handler(callback=cmd_delete_item, commands='удалить')
    dp.register_callback_query_handler(del_callback, lambda x: x.data and x.data.startswith('del '))
