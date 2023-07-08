from aiogram.utils import executor
from handlers import admin_handlers, client_handlers, abuse_filter
from data_base import sqlite_db
from tg_bot import dp


async def startup_func(_):
    print("Бот запущен.")
    sqlite_db.sql_start()
    print("База данных запущена.")


async def shutdown_func(_):
    print("Бот завершил работу.")


admin_handlers.register_handlers_admin(dp)
client_handlers.register_handlers_client(dp)
abuse_filter.register_handlers_abuse_filter(dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=startup_func, on_shutdown=shutdown_func)
