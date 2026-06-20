from pprint import pprint
import requests
import json


def chek_key(dict, key, nummer = 0):
    while key in dict:
        if nummer != 0:
            key = key[:-3]
        if nummer > 9:
            key = key[:-4]
        nummer += 1
        key = key + str(f"({nummer})")
        chek_key(dict, key, nummer)
    return key


TOKEN = input("Введите токен: ")

headers = {
    'Authorization': f"OAuth {TOKEN}",
}

text = input("Введите текст надписи:")

response = requests.get(f"https://cataas.com/cat/says/{text}?json=true")
requests.post(f"https://cloud-api.yandex.net/v1/disk/resources/upload?path=/FPY-152/{text}&url={response.json()['url']}", headers=headers)

with open("Cats_info.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
    text = chek_key(json_data, text)
    json_data.setdefault(text, dict(response.headers)['Content-Length'])

with open("Cats_info.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False)