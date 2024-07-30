marks = [
    {"name": "Toyota", "producer_country_name": "Япония"},
    {"name": "Honda", "producer_country_name": "Япония"},
    {"name": "Ford", "producer_country_name": "Америка"},
    {"name": "BMW", "producer_country_name": "Германия"},
    {"name": "Audi", "producer_country_name": "Германия"},
    {"name": "Mercedes", "producer_country_name": "Германия"},
    {"name": "Changan", "producer_country_name": "Китай"},
    {"name": "Hyundai", "producer_country_name": "Южная корея"},
    {"name": "Renault", "producer_country_name": "Франция"},
    {"name": "Chevrolet", "producer_country_name": "Америка"},
]

models = [
    {"name": "Corolla", "mark": 1},
    {"name": "Civic", "mark": 2},
    {"name": "Focus", "mark": 3},
    {"name": "X5", "mark": 4},
    {"name": "A4", "mark": 5},
    {"name": "A-CLASS", "mark": 6},
    {"name": "CS55PLUS", "mark": 7},
    {"name": "Elantra", "mark": 8},
    {"name": "Duster", "mark": 9},
    {"name": "Camaro", "mark": 10},
]

parts_names = [
    "Бампер",
    "Капот",
    "Дверь",
    "Порог",
    "Крыло",
    "Сидение",
    "Зеркало салонное",
    "Рамка магнитолы",
    "Обшивка стойки кузова",
    "Обшивка двери багажника",
]
colors = ["красный", "синий", "зелёный", "чёрный", "белый", None]


def _create_marks() -> None:
    """Заполнить таблицу марками автомобилей."""
    for mark_data in marks:
        try:
            mark, _ = Mark.objects.get_or_create(
                name=mark_data["name"], defaults=mark_data
            )
            mark.save()
        except Exception as ex:
            print(
                f"Ошибка добавления марки автомобиля в базу {mark_data['name']}: {ex}"
            )
    print("Марки автомобилей были добавлены в базу.")


def _create_models() -> None:
    """Заполнить таблицу моделями автомобилей."""
    for model_data in models:
        try:
            mark = Mark.objects.get(id=model_data["mark"])
            model, _ = Model.objects.get_or_create(
                name=model_data["name"],
                mark=mark,
                defaults={
                    "mark": mark,
                },
            )
            model.save()
        except Exception as ex:
            print(
                f"Ошибка добавления модели автомобиля в базу {model_data["name"]}: {ex}"
            )
    print("Модели автомобилей были добавлены в базу.")


def _create_parts() -> None:
    """Заполнить таблицу запчастями."""
    marks = list(Mark.objects.all())
    models = list(Model.objects.all())

    for _ in range(10_000):
        try:
            part_name = random.choice(parts_names)
            mark = random.choice(marks)
            model = random.choice([m for m in models if m.mark == mark])
            price = round(random.uniform(500.0, 8_000.0), 2)
            json_data = {
                "color": random.choice(colors),
                "is_new_part": random.choice([True, False, None]),
                "count": random.randint(1, 5),
            }

            part = Part.objects.create(
                name=part_name,
                mark=mark,
                model=model,
                price=price,
                json_data=json_data,
            )
            part.save()
        except Exception as ex:
            print(f"Ошибка добавления запчастей в базу: {ex}")
    print("Запчасти были добавлены в базу.")


def main():
    _create_marks()
    _create_models()
    _create_parts()


if __name__ == "__main__":
    import os
    import random
    import sys

    import django

    sys.path.append(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")
    )

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    django.setup()

    from parts.models import Mark, Model, Part

    print("Добавление таблиц в базу...")
    main()
    print("Добавление таблиц в базу прошло успешно.")
