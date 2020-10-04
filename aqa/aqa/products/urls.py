from django.urls import path

from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
)

app_name = "products"
urlpatterns = [
    path("", ProductListCreateView.as_view()),
    path("<int:pk>/", ProductRetrieveUpdateDestroyView.as_view()),
]