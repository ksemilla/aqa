from django.urls import path

from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
    ProductQueryView,
)

app_name = "products"

# api/products/
urlpatterns = [
    path("", ProductListCreateView.as_view()),
    path("<int:pk>/", ProductRetrieveUpdateDestroyView.as_view()),
    path("search/", ProductQueryView.as_view()),
]