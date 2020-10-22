from django.urls import path

from .views import (
    CustomerListCreateView,
    # CustomerRetrieveUpdateDestroyView,
)

app_name = "customers"

# api/customers/
urlpatterns = [
    path("", CustomerListCreateView.as_view()),
    # path("<int:pk>/", CustomerRetrieveUpdateDestroyView.as_view()),
]