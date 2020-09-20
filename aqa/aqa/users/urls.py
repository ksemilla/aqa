from django.urls import path

from aqa.users.views import (
    # user_detail_view,
    # user_redirect_view,
    # user_update_view,
    UserListCreateView
)

app_name = "users"
urlpatterns = [
    path("", UserListCreateView.as_view()),
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
