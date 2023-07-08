from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

load_button = KeyboardButton(text='/загрузить')
delete_button = KeyboardButton(text='/удалить')
cancel_button = KeyboardButton(text='/отменить')
menu_button = KeyboardButton(text='/меню')

kb_admin.row(load_button, cancel_button, delete_button)
kb_admin.add(menu_button)
