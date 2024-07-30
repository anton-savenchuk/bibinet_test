from django.urls import path

from .views import MarkListView


urlpatterns = [
    path("marks/", MarkListView.as_view(), name="marks"),
]
