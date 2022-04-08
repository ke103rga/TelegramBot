import json

words =[]
json_file_name = "D:\прог_Питон\PycharmProjects\\tg_bot\other_tools\words_json"
txt_file_name = "D:\прог_Питон\PycharmProjects\\tg_bot\other_tools\\bad_words.txt"

with open(file=txt_file_name, mode='r', encoding="UTF-8") as file:
    for str in file:
        words.extend(list(map(lambda s: s.strip('\n'), str.split())))


with open(file=json_file_name, mode="w") as new_file:
    json.dump(words, new_file)




