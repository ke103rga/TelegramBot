from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import admin_first_check_kb, admin_change_able_kb, admin_dinamic_change_kb, admin_category_choise_kb
from aiogram.types import chat_member
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



class FSMAdmin(StatesGroup):
    password = State()
    change_able = State()
    photo = State()
    name = State()
    category = State()
    description = State()
    price = State()
    change_check = State()
    dinamic_correctives = State()


ID = None
PASSWORD = "11"


# @dp.message_handler(lambda member: chat_member.ChatMember.is_chat_admin or chat_member.ChatMember.is_chat_admin,
#                  commands=['moderator'], state=None)
async def command_make_changes(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Введите пароль чтобы получить возможность вносить изменения")
    await FSMAdmin.password.set()
    await message.delete()


# @dp.message_handler(state=FSMAdmin.password)
async def checked_password(message: types.Message, state: FSMContext):
    if message.text == PASSWORD:
        await bot.send_message(message.from_user.id, "Вы хотите внести изменения?",
                               reply_markup=admin_change_able_kb)
        await FSMAdmin.change_able.set()
        await message.delete()
    else:
        await bot.send_message(message.from_user.id, "Вы ввели неверный пароль")
        await state.finish()


# начало диалога с администратором (сообщение с командной "добавить")
# @dp.message_handler(commands=['Добавить'], state=FSMAdmin.change_able)
async def command_add(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply(text="Загрузите фото")
    else:
        await bot.send_message(message.from_user.id, "Вы не являетесь администратором группы")


# Отслеживаем ответ и продолжаем диалог просьбой дать название
# @dp.message_handler(state=FSMAdmin.photo, content_types=['photo'])
async def photo_load(message: types.Message, state: FSMContext):
    if (message.from_user.id == ID):
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            if len(data.keys()) > 1:
                await show_change(message, data)
                await message.answer(text="Данные успешно введены\nВсе верно?",
                                     reply_markup=admin_first_check_kb)
                await FSMAdmin.change_check.set()
            else:
                await FSMAdmin.next()
                await message.reply(text="Введите название")
    else:
        await bot.send_message(message.from_user.id, "Вы не являетесь администратором группы")


# Следующий шаг добавить описание
# @dp.message_handler(state=FSMAdmin.name)
async def name_load(message: types.Message, state: FSMContext):
    if (message.from_user.id == ID):
        async with state.proxy() as data:
            data['name'] = message.text
            if len(data.keys()) > 2:
                await show_change(message, data)
                await message.answer(text="Данные успешно введены\nВсе верно?",
                                     reply_markup=admin_first_check_kb)
                await FSMAdmin.change_check.set()
            else:
                await FSMAdmin.next()
                await message.reply(text="Укажите категорию", reply_markup=admin_category_choise_kb)
    else:
        await bot.send_message(message.from_user.id, "Вы не являетесь администратором группы")


# @dp.message_handler(state=FSMAdmin.category)
async def category_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
        if len(data.keys()) > 3:
            await show_change(message, data)
            await message.answer(text="Данные успешно введены\nВсе верно?",
                                 reply_markup=admin_first_check_kb)
            await FSMAdmin.change_check.set()
        else:
            await FSMAdmin.next()
            await message.reply(text="добавьте описание")


# Добавляем описание
# @dp.message_handler(state=FSMAdmin.description)
async def desc_load(message: types.Message, state: FSMContext):
    if (message.from_user.id == ID):
        async with state.proxy() as data:
            data['description'] = message.text
            if len(data.keys()) > 4:
                await show_change(message, data)
                await message.answer(text="Данные успешно введены\nВсе верно?",
                                     reply_markup=admin_first_check_kb)
                await FSMAdmin.change_check.set()
            else:
                await FSMAdmin.next()
                await message.reply(text="Укажите цену")
    else:
        await bot.send_message(message.from_user.id, "Вы не являетесь администратором группы")


# уведомляем администратора об успешном введении всех данных
# @dp.message_handler(state=FSMAdmin.price)
async def price_load(message: types.Message, state: FSMContext):
    if (message.from_user.id == ID):
        async with state.proxy() as data:
            data['cost'] = float(message.text)
            await bot.send_photo(photo=data['photo'],
                                 caption=f"<b>{data['name']}</b>"
                                         f"{data['category']}"
                                         f"\n{data['description']}"
                                         f"\n<i>{data['cost']}</i>",
                                 parse_mode=types.ParseMode.HTML,
                                 chat_id=message.from_user.id)
        await message.answer(text="Данные успешно введены\nВсе верно?",
                             reply_markup=admin_first_check_kb)
        await FSMAdmin.change_check.set()
    else:
        await bot.send_message(message.from_user.id, "Вы не являетесь администратором группы")


# Проверка введенных изменнений
@dp.message_handler(lambda message: message.text.lower() == "все верно", state=FSMAdmin.change_check)
async def confrim_changes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Перенос изменений в базу данных и очищение оперативной памяти
        await sqlite_db.data_base_add(state)
        data.clear()
    await state.finish()


@dp.message_handler(lambda message: message.text == "Необходимы исправления", state=FSMAdmin.change_check)
async def unconfrim_changes(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Что необходимо изменить?",
                           reply_markup=admin_dinamic_change_kb)
    await FSMAdmin.dinamic_correctives.set()


@dp.message_handler(state=FSMAdmin.dinamic_correctives)
async def dinamic_correctives(message: types.Message):
    if message.text == "Фото" or message.text == "Все":
        await FSMAdmin.photo.set()
    elif message.text == "Категория":
        await FSMAdmin.category.set()
    elif message.text == "Название":
        await FSMAdmin.name.set()
    elif message.text == "Описание":
        await FSMAdmin.description.set()
    elif message.text == "Цена":
        await FSMAdmin.price.set()


# Возможность прервать и отменить ввод данных
# @dp.message_handler(state="*", commands=['Отмена'])
# @dp.message_handler(lambda message: message.text.lower() == "отмена", state="*")
async def command_stop(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply("Вы не находились в режиме внесения изменений")
        return
    await state.finish()
    await message.reply("Ок")


async def command_del_menu_elem(message: types.Message):
    if message.from_user.id == ID:
        data = sqlite_db.data_read_list()
        for elem in data:
            await bot.send_photo(photo=elem[0],
                                 caption=f"<b>{elem[1]}</b>"
                                         f"\n{elem[2]}"
                                         f"\n{elem[3]}"
                                         f"\n<i>{elem[4]}</i>",
                                 parse_mode=types.ParseMode.HTML,
                                 chat_id=message.from_user.id)
            await bot.send_message(message.from_user.id, text="^^^",
                                   reply_markup=InlineKeyboardMarkup().
                                   add(InlineKeyboardButton("Удалить", callback_data=f"del {elem[1]}")))


@dp.callback_query_handler(lambda callback_data: callback_data.data.startswith('del'))
async def delete_elem(callback_query: types.CallbackQuery):
    print("it's still working")
    await sqlite_db.data_base_delete(callback_query.data.replace("del ", ""))
    await bot.answer_callback_query(callback_query_id=callback_query.id,
                                    text=f"{callback_query.data.replace('del ', '')} удалена из меню",
                                    show_alert=True, cache_time=0.000001)
    # await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} удалена из меню", show_alert=True)


async def show_change(message: types.Message, data):
    await bot.send_photo(photo=data['photo'],
                         caption=f"<b>{data['name']}</b>\n"
                                 f"{data['category']}"
                                 f"\n{data['description']}"
                                 f"\n<i>{data['cost']}</i>",
                         parse_mode=types.ParseMode.HTML,
                         chat_id=message.from_user.id)


def register_handler_admin(dp: Dispatcher):
    dp.callback_query_handler(delete_elem, Text(startswith="del"), state="*")

    dp.register_message_handler(command_make_changes, lambda
        member: chat_member.ChatMember.is_chat_admin or chat_member.ChatMember.is_chat_admin,
                                commands=['moderator'], state=None)

    dp.register_message_handler(checked_password, state=FSMAdmin.password)

    dp.register_message_handler(command_make_changes, lambda
        member: chat_member.ChatMember.is_chat_admin or chat_member.ChatMember.is_chat_admin,
                                commands=['moderator'], state=None)

    dp.register_message_handler(checked_password, lambda
        member: chat_member.ChatMember.is_chat_admin or chat_member.ChatMember.is_chat_admin,
                                state=FSMAdmin.password)

    dp.register_message_handler(command_add, commands=['Добавить'], state=FSMAdmin.change_able)

    dp.register_message_handler(command_del_menu_elem, commands=['Удалить'], state=FSMAdmin.change_able)

    dp.register_message_handler(command_stop, state="*", commands=['Отмена'])

    dp.register_message_handler(command_stop, lambda message: message.text.lower() == "отмена", state="*")

    dp.register_message_handler(photo_load, state=FSMAdmin.photo, content_types=['photo'])

    dp.register_message_handler(name_load, state=FSMAdmin.name)

    dp.register_message_handler(category_load, state=FSMAdmin.category)

    dp.register_message_handler(desc_load, state=FSMAdmin.description)

    dp.register_message_handler(price_load, state=FSMAdmin.price)


