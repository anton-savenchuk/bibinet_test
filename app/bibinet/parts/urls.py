from django.urls import path

from .views import MarkListView, ModelListView


urlpatterns = [
    path("marks/", MarkListView.as_view(), name="marks"),
    path("models/", ModelListView.as_view(), name="models"),
]
