from django.urls import path

from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDestroy,
)

app_name = "products"
urlpatterns = [
    path("", ProductListCreateView.as_view()),
    path("<int:pk>/", ProductRetrieveUpdateDestroy.as_view()),
]