from rest_framework.pagination import PageNumberPagination


class CustomerPageNumberPagination(PageNumberPagination):
    page_size = 20
