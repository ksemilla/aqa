from django.urls import path

from aqa.users.views import (
    # user_detail_view,
    # user_redirect_view,
    # user_update_view,
    UserListView,
    UserCreateView,
    UserRetrieveUpdateDestroyView,
    RoleListView,
)

app_name = "users"

# api/users/
urlpatterns = [
    path("", UserListView.as_view()),
    path("signup/", UserCreateView.as_view()),
    path('<int:user_pk>/', UserRetrieveUpdateDestroyView.as_view()),
    path('roles/', RoleListView.as_view()),
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
