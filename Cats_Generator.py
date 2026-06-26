from pprint import pprint
import requests
import json
import time

TOKEN = input("Введите токен: ")

headers = {
    'Authorization': f"OAuth {TOKEN}",
}

text = input("Введите текст надписи:")

response = requests.get(f"https://cataas.com/cat/says/{text}?json=true")
response_check = requests.post(f"https://cloud-api.yandex.net/v1/disk/resources/upload?path=/FPY-152/{text}&url={response.json()['url']}", headers=headers)

while requests.get(response_check.json()['href'], headers=headers).json()['status'] != 'success':
    print('Loading')
    time.sleep(3)



with open("Cats_info.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
    nummer = 0
    while text in json_data:
        if nummer > 0:
            text = text[:-3]
        elif nummer > 9:
            text = text[:-4]
        nummer += 1
        text = text + str(f"({nummer})")

    name = text

    if nummer > 0:
        print(name)
        if nummer > 9:
            name = name[:-4]
        else:
            name = name[:-3]
        print(name)
        check_size = requests.get(f"https://cloud-api.yandex.net/v1/disk/resources?path=/FPY-152/{name}%20({nummer})", headers=headers)
    else:
        check_size = requests.get(f"https://cloud-api.yandex.net/v1/disk/resources?path=/FPY-152/{name}", headers=headers)
    pprint(check_size.json()["size"])
    json_data.setdefault(text, check_size.json()["size"])

with open("Cats_info.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False)