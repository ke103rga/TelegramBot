from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

but_ok = KeyboardButton("Все верно")
but_incorrect = KeyboardButton("Необходимы исправления")

but_add = KeyboardButton("/Добавить")
but_cansel = KeyboardButton("/Отмена")
but_delete = KeyboardButton("/Удалить")

but_photo = KeyboardButton("Фото")
but_name = KeyboardButton("Название")
but_description = KeyboardButton("Описание")
but_price = KeyboardButton("Цена")
but_category = KeyboardButton("Категория")
but_all_elements = KeyboardButton("Все")

but_category_drinks = KeyboardButton("Напитки")
but_category_pizza = KeyboardButton("Пицца")
but_category_snacks = KeyboardButton("Закуски")

admin_first_check_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but_ok, but_incorrect]],
                                           one_time_keyboard=True)

admin_change_able_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but_add, but_delete], [but_cansel]],
                                           one_time_keyboard=True)

admin_dinamic_change_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but_category], [but_photo, but_name], [but_description, but_price], [but_all_elements]],
                                              one_time_keyboard=True)

admin_category_choise_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but_category_pizza, but_category_snacks, but_category_drinks]],
                                               one_time_keyboard=True)



