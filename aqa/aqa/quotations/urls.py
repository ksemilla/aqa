from django.urls import path

from .views import (
    QuotationSampleView,
    QuotationFetchUpdateDestroy
)

app_name = "quotations"
urlpatterns = [
    path("", QuotationSampleView.as_view()),
    path("<int:pk>/", QuotationFetchUpdateDestroy.as_view()),
]
