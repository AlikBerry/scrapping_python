from django.urls import path
from .views import ApiIndexView, ScraperView


urlpatterns = [
    path("api/", ApiIndexView.as_view(), name="index"),
    path("result/", ScraperView.as_view(), name="scraper"),
]