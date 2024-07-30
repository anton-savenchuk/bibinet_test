from django.db import models


class Mark(models.Model):
    """Модель марки автомобиля"""

    name = models.CharField(max_length=255, verbose_name="Марка автомобиля")
    producer_country_name = models.CharField(
        max_length=255, verbose_name="Страна производителя"
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать")

    def __str__(self) -> str:
        """Возвращает строковое представление объекта в виде имени марки автомобиля."""
        return self.name

    class Meta:
        """Сортировка, название модели в админ-панели, таблица с данными."""

        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name", "producer_country_name", "is_visible"])
        ]


class Model(models.Model):
    """Модель модели автомобиля"""

    name = models.CharField(max_length=255, verbose_name="Модель автомобиля")
    mark = models.ForeignKey(
        to=Mark, on_delete=models.CASCADE, verbose_name="Марка автомобиля"
    )
    is_visible = models.BooleanField(default=True, verbose_name="Показывать")

    def __str__(self) -> str:
        """Возвращает строковое представление объекта в виде имени модели автомобиля."""
        return self.name

    class Meta:
        """Сортировка, название модели в админ-панели, таблица с данными."""

        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модели автомобилей"
        ordering = ["name"]
        indexes = [models.Index(fields=["name", "mark", "is_visible"])]


class Part(models.Model):
    """Модель запчасти."""

    name = models.CharField(max_length=255, verbose_name="Название запчасти")
    mark = models.ForeignKey(
        to=Mark, on_delete=models.CASCADE, verbose_name="Марка автомобиля"
    )
    model = models.ForeignKey(
        to=Model, on_delete=models.CASCADE, verbose_name="Модель автомобиля"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость запчасти"
    )
    json_data = models.JSONField(default=dict, blank=True)
    is_visible = models.BooleanField(default=True, verbose_name="Показывать")

    def __str__(self) -> str:
        """Возвращает строковое представление объекта в виде имени запчасти."""
        return self.name

    class Meta:
        """Сортировка, название модели в админ-панели, таблица с данными."""

        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"
        ordering = ["name", "mark", "model", "price"]
        indexes = [
            models.Index(
                fields=["name", "mark", "model", "price", "is_visible"]
            )
        ]
