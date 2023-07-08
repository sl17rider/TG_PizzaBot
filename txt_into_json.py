import json


with open(file='obscene_words.txt', mode='r', encoding='utf8') as file:
    data = file.readlines()
    data = [word.strip() for word in data if word.strip()]


with open(file='obscene_words.json', mode='w') as file:
    json.dump(data, file)


print('Конвертация содержимого из файла txt в файл JSON завершена.')
