from create_bot import bot, dp
from aiogram import Dispatcher
import json
import string
from other_tools import File
from aiogram import types


json_file_name = "D:\прог_Питон\PycharmProjects\\tg_bot\other_tools\words_json"
txt_file_name = "D:\прог_Питон\PycharmProjects\\tg_bot\other_tools\\bad_words.txt"


# @dp.message_handler()
async def words_check(message: types.Message):
    message_words_set = {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split()}
    bad_words_set = set(json.load(open(json_file_name, 'r')))
    bad_words = message_words_set.intersection(bad_words_set)

    if message.text.startswith("*"):
        with open(json_file_name, 'w') as json_file:
            json.dump([message.text[1:]], json_file)
        with open(txt_file_name, 'a', encoding="UTF-8") as txt_file:
            print(message.text[1:] + ' ', file=txt_file)
        await message.delete()

    if bad_words != set():
        new_message = message.text
        for word in bad_words:
            new_message = new_message.replace(word.translate(str.maketrans("", "", string.punctuation)), word[:2] + '*' * (len(word) - 2))
        await message.reply(new_message + "\nМатериться, сучара, здесь могу только я")
        await message.delete()


def register_handler_mat(dp: Dispatcher):
    dp.register_message_handler(words_check)
