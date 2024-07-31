from django.urls import path

from .views import MarkListView, ModelListView, PartSearchJsonView


urlpatterns = [
    path("marks/", MarkListView.as_view(), name="marks"),
    path("models/", ModelListView.as_view(), name="models"),
    path(
        "api/search/part/",
        PartSearchJsonView.as_view(),
        name="search_part_json",
    ),
]
