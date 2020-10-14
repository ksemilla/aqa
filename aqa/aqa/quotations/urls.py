from django.urls import path

from .views import (
    QuotationListCreateView,
    QuotationRetrieveUpdateDestroyView,
    QuotationItemListCreateView,
    QuotationItemRetrieveUpdateDestroyView,
)

app_name = "quotations"

# api/quotations/
urlpatterns = [
    path("", QuotationListCreateView.as_view()),
    path("<int:quotation_pk>/", QuotationRetrieveUpdateDestroyView.as_view()),
    path("items/", QuotationItemListCreateView.as_view()),
    path("items/<int:quotation_item_pk>/", QuotationItemRetrieveUpdateDestroyView.as_view()),   
]
