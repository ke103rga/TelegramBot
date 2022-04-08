from aiogram import types
from aiogram.dispatcher import Dispatcher
from create_bot import bot, dp
from keyboards import order_kb, client_kb
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSMClient(StatesGroup):
    start_making_order = State()
    confrimed_order = State()
    payment = State() # TODO

# Все функции декораторы необходимы лишь в случание написания проекта в одном файле
# Нижепрописанные функции, содержащие декораторы могут быть вызвыны в основном
# файле, запускающем бота, но правильнее это будет оформить через метод
# register_handler()


orders = {}


# @ dp.message_handler(commands=["make_order"], state=None)
async def command_start_making_order(message: types.Message):
    menu = sqlite_db.data_read_list()
    await FSMClient.start_making_order.set()
    for elem in menu:
        await bot.send_photo(photo=elem[0],
                             caption=f"<b>{elem[1]}</b>"
                                     f"\n{elem[2]}"
                                     f"\n{elem[3]}"
                                     f"\n<i>{elem[4]}</i>",
                             parse_mode=types.ParseMode.HTML,
                             chat_id=message.from_user.id)
        await bot.send_message(message.from_user.id, text="^^^",
                               reply_markup=InlineKeyboardMarkup().
                               add(InlineKeyboardButton("Добавить в заказ", callback_data=f"add {elem[1]}")))
    await bot.send_message(message.from_user.id, text="Вы готовы сделать заказ?",
                           reply_markup=order_kb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('add'),
                           state=FSMClient.start_making_order)
async def add_to_order(callback_query: types.CallbackQuery):
    menu = sqlite_db.data_read_dict()
    print("an element was added to current order")
    user_id = callback_query.from_user.id
    if user_id in orders.keys():
        orders[user_id].append(menu[callback_query.data.replace("add ", "")])
    else:
        orders[user_id] = [menu[callback_query.data.replace("add ", "")]]
    # await callback_query.answer(text=f'callback_query.data.replace("add ", "") добавлена в заказ', show_alert=True)
    await bot.answer_callback_query(callback_query_id=callback_query.id,
                                    text=f"{callback_query.data.replace('add ', '')} добавлен в заказ",
                                    show_alert=True, cache_time=0.000001)


async def command_change_order(message: types.Message):
    user_id = message.from_user.id
    user_order = orders[user_id]
    for elem in user_order:
        await bot.send_photo(photo=elem[0],
                             caption=f"<b>{elem[1]}</b>"
                                     f"\n{elem[2]}"
                                     f"\n{elem[3]}"
                                     f"\n<i>{elem[4]}</i>",
                             parse_mode=types.ParseMode.HTML,
                             chat_id=message.from_user.id,
                             reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Удалить из заказа",
                                                                                          callback_data=f"del_from_order {elem['name']}")))
    await bot.send_message(text="Всё готово?", reply_markup=order_kb)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('del_from_order'),
                           state=FSMClient.start_making_order)
async def del_from_order(message: types.Message, callback_query: types.CallbackQuery):
    user_id = message.from_user.id
    user_order = orders[user_id]
    user_order.remove(callback_query.data.replace("del_from_order ", ""))



async def command_show_order(message: types.Message):
    user_id = message.from_user.id
    user_order = orders[user_id]
    for elem in user_order:
        await show_user_order(message, elem)
    await FSMClient.confrimed_order.set()


async def command_cansel_order(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    del orders[user_id]
    await state.finish()


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Ну здарова...", reply_markup=client_kb)
        await message.delete()
    except:
        await message.reply("Общение с ботом в лс\nНапишите ему:\nhttps://web.telegram.org/z/#5183698640")
        await message.delete()


async def command_location(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="ул. Кузнецова, д. 23, 1 этаж")
    await message.delete()



async def command_work_time(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="пн - пт: 8:30 - 19:00\nсб - вс: 10:30 - 19:00")
    await message.delete()


async def command_mat_check(message: types.Message):
    await message.answer(text="Чтобы сообщить об использовании ненормативной лексики "
                          "введите сообщение в формате <b>*'использованный мат'</b>\n"
                          "И это слово никогда больше не появится в данном чате!",
                         parse_mode=types.ParseMode.HTML)
    await message.delete()


async def command_menu(message: types.Message):
    await sqlite_db.data_base_read(message)


async def show_user_order(message: types.Message, data):
    await bot.send_photo(photo=data['photo'],
                         caption=f"<b>{data['name']}</b>\n"
                                 f"{data['category']}"
                                 f"\n{data['description']}"
                                 f"\n<i>{data['cost']}</i>",
                         parse_mode=types.ParseMode.HTML,
                         chat_id=message.from_user.id)


def register_handler_client(dp: Dispatcher):
    dp.callback_query_handler(add_to_order, lambda callback_query: callback_query.data.startswith('add'), state="*")
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_location, commands=['location'])
    dp.register_message_handler(command_work_time, commands=['work_time'])
    dp.register_message_handler(command_mat_check, commands=['mat_control'])
    dp.register_message_handler(command_menu, commands=['menu'])
    dp.register_message_handler(command_start_making_order, commands=['make_order'])
    dp.register_message_handler(command_show_order, commands=['Оформить_заказ'])#, state=FSMClient.start_making_order)
    dp.register_message_handler(command_change_order, commands=['Изменить_заказ'], state=FSMClient.start_making_order)
    dp.register_message_handler(command_cansel_order, commands=['Отменить_заказ'], state=FSMClient.start_making_order)


