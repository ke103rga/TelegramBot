from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


but_start = KeyboardButton("/start")
but_loc = KeyboardButton("/location")
but_work_time = KeyboardButton("/work_time")
but_mat_control = KeyboardButton("/mat_control")
but_menu = KeyboardButton("/menu")
but_make_order = KeyboardButton("/make_order")

but_finish_order_making = KeyboardButton("/Оформить_заказ")
but_cancel_order_making = KeyboardButton("/Отменить_заказ")
but_change_order = KeyboardButton("/Изменить_заказ")


client_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but_menu, but_make_order],
                                                                [but_start, but_loc],
                                                                [but_work_time, but_mat_control]],
                                one_time_keyboard=True)


order_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but_change_order], [but_finish_order_making, but_cancel_order_making]],
                               one_time_keyboard=True)
# client_kb.row(but_mat_control, but_work_time)
