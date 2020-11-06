from rest_framework.pagination import PageNumberPagination


class UserPageNumberPagination(PageNumberPagination):
    page_size = 20
