from rest_framework.pagination import PageNumberPagination


class QuotationPageNumberPagination(PageNumberPagination):
    page_size = 20


class QuotationItemPageNumberPagination(PageNumberPagination):
    page_size = 20
