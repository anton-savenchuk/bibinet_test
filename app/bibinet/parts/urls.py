from django.urls import path

from .views import (
    MarkListView,
    ModelListView,
    PartSearchJsonView,
    PartSearchView,
)


urlpatterns = [
    path("marks/", MarkListView.as_view(), name="marks"),
    path("models/", ModelListView.as_view(), name="models"),
    path("search/part/", PartSearchView.as_view(), name="search_part"),
    path(
        "api/search/part/",
        PartSearchJsonView.as_view(),
        name="search_part_json",
    ),
]
