import json

import requests


url = "http://localhost:8000/api/search/part/"

# Пример данных для поиска
# data = {
#     "mark_name": "Honda",
#     "part_name": "Бампер",
#     "params": {"color": "чёрный"},
#     "page": 1,
# }
data = {
    "mark_list": [1, 3],
    "part_name": "бамп",
    "params": {"is_new_part": False, "color": "белый"},
    "price_gte": 2000,
    "price_lte": 5000,
    "page": 1,
}

headers = {
    "Content-Type": "application/json",
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print(
        json.dumps(
            response.json(), ensure_ascii=False, indent=4, sort_keys=True
        )
    )
else:
    print(f"Error: {response.status_code}")
    print(response.text)
