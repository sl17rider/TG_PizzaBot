import sqlite3 as sq
from tg_bot import bot

global base, cur


def sql_start():
    global base, cur
    base = sq.connect(database='pizza_cool.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def sql_add_item(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n\nОписание: {ret[2]}\nЦена: {ret[3]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_item(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
