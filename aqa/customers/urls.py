from django.urls import path

from .views import (
    CustomerListCreateView,
    CustomerRetrieveUpdateDestroyView,
    CustomerQueryView,
    ContactPersonListCreateView,
    ContactPersonRetrieveUpdateDestroyView,
    ContactPersonQueryView,
    AddressListCreateView,
    AddressRetrieveUpdateDestroyView,
    AddressQueryView,   
)

app_name = "customers"

# api/customers/
urlpatterns = [
    path("", CustomerListCreateView.as_view()),
    path("<int:customer_pk>/", CustomerRetrieveUpdateDestroyView.as_view()),
    path("search/", CustomerQueryView.as_view()),
    path("<int:customer_pk>/contact/", ContactPersonListCreateView.as_view()),
    path("<int:customer_pk>/contact/<int:contact_pk>/", ContactPersonRetrieveUpdateDestroyView.as_view()),
    path("<int:customer_pk>/contact/search/", ContactPersonQueryView.as_view()),
    path("<int:customer_pk>/address/", AddressListCreateView.as_view()),
    path("<int:customer_pk>/address/<int:address_pk>/", AddressRetrieveUpdateDestroyView.as_view()),
    path("<int:customer_pk>/address/search/", AddressQueryView.as_view()),

]