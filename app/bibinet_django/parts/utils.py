from core.settings import PAGINATION_RANGE


menu = [
    {"title": "Марки автомобилей", "url_name": "marks"},
    {"title": "Модели автомобилей", "url_name": "models"},
    {"title": "Поиск запчастей", "url_name": "search_part"},
]


class DataMixin:
    """Mixin, который можно использовать в качестве контекста шаблона."""

    paginate_by = PAGINATION_RANGE

    def get_user_context(self, **kwargs):
        """Вернуть словарь для использования в качестве контекста шаблона."""
        context = kwargs
        context["menu"] = menu

        return context
