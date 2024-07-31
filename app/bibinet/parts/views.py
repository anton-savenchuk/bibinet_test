import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .models import Mark, Model, Part
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


@method_decorator(csrf_exempt, name="dispatch")
class PartSearchJsonView(DataMixin, ListView):
    model = Part
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        """Вернуть обработанный POST-запрос."""
        self.data = json.loads(request.body)
        self.page_number = self.data.get("page", 1)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Вернуть словарь для использования в качестве контекста шаблона."""
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title="Поиск запчастей")
        context |= user_context
        results = [
            {
                "mark": {
                    "id": part.mark.id,
                    "name": part.mark.name,
                    "producer_country_name": part.mark.producer_country_name,
                },
                "model": {"id": part.model.id, "name": part.model.name},
                "name": part.name,
                "json_data": part.json_data,
                "price": part.price,
            }
            for part in context["page_obj"]
        ]

        response_data = {
            "response": results,
            "count": context["paginator"].count,
            "summ": sum(
                part.price for part in context["paginator"].object_list
            ),
        }

        return response_data

    def get_queryset(self):
        """Вернуть список элементов для этого представления с учетом
        фильтров из данных запроса."""
        queryset = Part.objects.filter(is_visible=True)

        if "mark_name" in self.data:
            queryset = queryset.filter(
                mark__name__icontains=self.data["mark_name"]
            )
        if "part_name" in self.data:
            queryset = queryset.filter(name__icontains=self.data["part_name"])
        if "params" in self.data:
            params = self.data["params"]
            if "color" in params:
                queryset = queryset.filter(json_data__color=params["color"])
            if "is_new_part" in params:
                is_new_part = params["is_new_part"]
                queryset = queryset.filter(json_data__is_new_part=is_new_part)
        if "price_gte" in self.data:
            queryset = queryset.filter(price__gte=self.data["price_gte"])
        if "price_lte" in self.data:
            queryset = queryset.filter(price__lte=self.data["price_lte"])

        return queryset

    def render_to_response(self, context, **response_kwargs):
        """Вернуть данные в формате JSON."""
        return JsonResponse(self.get_context_data())


class PartSearchView(DataMixin, ListView):
    model = Part
    template_name = "parts/search_part.html"
    context_object_name = "parts"

    def get_context_data(self, **kwargs):
        """Вернуть словарь для использования в качестве контекста шаблона."""
        context = super().get_context_data(**kwargs)
        context["search_data"] = self.request.GET
        user_context = self.get_user_context(title="Поиск запчастей")

        return context | user_context

    def get_queryset(self):
        """Вернуть список элементов для этого представления с учетом
        фильтров из данных запроса."""
        queryset = Part.objects.filter(is_visible=True)
        mark_name = self.request.GET.get("mark_name")
        part_name = self.request.GET.get("part_name")
        color = self.request.GET.get("color")
        is_new_part = self.request.GET.get("is_new_part")
        price_gte = self.request.GET.get("price_gte")
        price_lte = self.request.GET.get("price_lte")

        if mark_name:
            queryset = queryset.filter(mark__name__icontains=mark_name)
        if part_name:
            queryset = queryset.filter(name__icontains=part_name)
        if color:
            queryset = queryset.filter(json_data__color__icontains=color)
        if is_new_part:
            is_new_part_bool = True if is_new_part.lower() == "true" else False
            queryset = queryset.filter(json_data__is_new_part=is_new_part_bool)
        if price_gte:
            queryset = queryset.filter(price__gte=price_gte)
        if price_lte:
            queryset = queryset.filter(price__lte=price_lte)

        return queryset
