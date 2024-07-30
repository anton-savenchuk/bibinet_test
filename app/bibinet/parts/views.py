from django.views.generic import ListView

from .models import Mark, Model
from .utils import DataMixin


class MarkListView(DataMixin, ListView):
    """Представление модели марки автомобиля."""

    model = Mark
    template_name = "mark_list.html"
    context_object_name = "marks"

    def get_context_data(self, **kwargs):
        """Вернуть словарь для использования в качестве контекста шаблона."""
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title="Марки автомобилей")

        return context | user_context

    def get_queryset(self):
        """Вернуть список элементов для этого представления."""
        return Mark.objects.filter(is_visible=True)


class ModelListView(DataMixin, ListView):
    """Представление модели модели автомобиля."""

    model = Model
    template_name = "model_list.html"
    context_object_name = "models"

    def get_context_data(self, **kwargs):
        """Вернуть словарь для использования в качестве контекста шаблона."""
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title="Модель автомобилей")

        return context | user_context

    def get_queryset(self):
        """Вернуть список элементов для этого представления."""
        return Model.objects.filter(is_visible=True)
