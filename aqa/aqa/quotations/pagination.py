from rest_framework.pagination import PageNumberPagination


class QuotationPageNumberPagination(PageNumberPagination):
    page_size = 10


class QuotationItemPageNumberPagination(PageNumberPagination):
    page_size = 5
