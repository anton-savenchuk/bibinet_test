## Первичная настройка

```bash
~ git clone https://github.com/anton-savenchuk/bibinet_test
~ cd bibinet_test
```

В папке приложения `app/bibinet/env` измените файл `.env.dev.example`, указав свои переменные окружения, и переименуйте его в `.env.dev`

## Сборка и запуск docker-compose

```bash
~ cd bibinet_test
~ docker-compose up --build 
```

После сборки проект доступен по ссылке [127.0.0.1:8000](http://127.0.0.1:8000/)

## Доступные адреса

- Марки автомобилей: [http://127.0.0.1:8000/marks/](http://127.0.0.1:8000/marks/),
- Модели автомобилей: [http://127.0.0.1:8000/models/](http://127.0.0.1:8000/models/),
- Поиск запчастей: [http://127.0.0.1:8000/search/part/](http://127.0.0.1:8000/search/part/).

## Наполнение базы тестовыми данными

```bash
~ docker exec -it bibinet_django bash
~ poetry run python scripts/generate_data_db.py
```

## Страница поиска запчастей

![](/search_page.png)

## POST запрос

Для поиска запчастей в **JSON** формате мажно вольпользоваться скриптом `scripts/request_json.py`

Пример запроса:

```json
data = {
    "mark_list": [1, 3],
    "part_name": "бамп",
    "params": {"is_new_part": False, "color": "белый"},
    "price_gte": 2000,
    "price_lte": 5000,
    "page": 1,
}
```

Пример ответа:

```json
{
    "response": [
        {
            "mark": {
                "id": 5,
                "name": "Audi",
                "producer_country_name": "Германия"
            },
            "model": {
                "id": 5,
                "name": "A4"
            },
            "name": "Бампер",
            "json_data": {
                "color": "белый",
                "count": 5,
                "is_new_part": false
            },
            "price": 3000.37
        },
        ...
        {
            "mark": {
                "id": 1,
                "name": "Toyota",
                "producer_country_name": "Япония"
            },
            "model": {
                "id": 1,
                "name": "Corolla"
            },
            "name": "Бампер",
            "json_data": {
                "color": "белый",
                "count": 3,
                "is_new_part": false
            },
            "price": 4362.74
        }
    ],
    "count": 30,
    "summ": 100872.35
}
```
