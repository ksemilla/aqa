from django.urls import path

from .views import (
    CustomerListCreateView,
    CustomerRetrieveUpdateDestroyView,
    CustomerQueryView,
    # ContactPersonListCreateView,
    # ContactPersonRetrieveUpdateDestroyView,
    # ContactPersonQueryView,
    # AddressListCreateView,
    # AddressRetrieveUpdateDestroyView,
    # AddressQueryView,   
)

app_name = "customers"

# api/customers/
urlpatterns = [
    path("", CustomerListCreateView.as_view()),
    path("<int:pk>/", CustomerRetrieveUpdateDestroyView.as_view()),
    path("search/", CustomerQueryView.as_view()),
    # path("contact/", ContactPersonListCreateView.as_view()),
    # path("contact/<int:pk>/", ContactPersonRetrieveUpdateDestroyView.as_view()),
    # path("contact/search/", ContactPersonQueryView.as_view()),
    # path("address/", AddressListCreateView.as_view()),
    # path("address/<int:pk>/", AddressRetrieveUpdateDestroyView.as_view()),
    # path("address/search/", AddressQueryView.as_view()),

]