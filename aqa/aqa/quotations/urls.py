from django.urls import path

from .views import (
    QuotationSampleView,
    QuotationFetchUpdateDestroy,

    QuotationListCreateView
)

app_name = "quotations"
urlpatterns = [
    path("", QuotationListCreateView.as_view()),
    path("<int:pk>/", QuotationFetchUpdateDestroy.as_view()),
]
