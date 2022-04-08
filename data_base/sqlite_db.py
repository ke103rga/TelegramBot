import sqlite3 as sq
from create_bot import bot
from aiogram import types


def sql_start():
    global base, cur
    base = sq.connect('pizza_menu')
    cur = base.cursor()
    if base:
        print("Bot connected with data base")
    base.execute('CREATE TABLE IF NOT EXISTS menu(photo TEXT, name TEXT PRIMARY KEY,'
                 ' category TEXT, description TEXT, price TEXT)')
    base.commit()


async def data_base_add(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def data_base_read(message):
    for data in base.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(photo=data[0],
                             caption=f"<b>{data[1]}</b>"
                                     f"\n{data[2]}"
                                     f"\n{data[3]}"
                                     f"\n<i>{data[4]}</i>",
                             parse_mode=types.ParseMode.HTML,
                             chat_id=message.from_user.id)


def data_read_dict():
    # return [elem for elem in base.execute('SELECT * FROM menu').fetchall()]

    list_menu = base.execute('SELECT * FROM menu').fetchall()
    dict_menu = {elem[1]: elem for elem in list_menu}
    return dict_menu


def data_read_list():
    return base.execute('SELECT * FROM menu').fetchall()


async def data_base_delete(name):
    cur.execute('DELETE FROM menu WHERE NAME == ?', (name,))
    base.commit()


