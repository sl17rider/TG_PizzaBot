from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_button = KeyboardButton(text='/меню')
schedule_button = KeyboardButton(text='/график')
location_button = KeyboardButton(text='/расположение')
contact_button = KeyboardButton(text='/контакты')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(menu_button)
kb_client.row(schedule_button, location_button, contact_button)
