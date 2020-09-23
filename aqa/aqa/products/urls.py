from django.urls import path

from .views import (
    ProductListCreateView,
    ProductFetchUpdateDestroy,
)

app_name = "products"
urlpatterns = [
    path("", ProductListCreateView.as_view()),
    path("<int:pk>/", ProductFetchUpdateDestroy.as_view()),
]