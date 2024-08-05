from django.urls import path

from .views import (
    get_index_page,
    MarkListView,
    ModelListView,
    PartSearchJsonView,
    PartSearchView,
)


urlpatterns = [
    path("", get_index_page, name="home"),
    path("marks/", MarkListView.as_view(), name="marks"),
    path("models/", ModelListView.as_view(), name="models"),
    path("search/part/", PartSearchView.as_view(), name="search_part"),
    path(
        "api/search/part/",
        PartSearchJsonView.as_view(),
        name="search_part_json",
    ),
]
