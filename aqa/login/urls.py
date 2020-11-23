from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    CustomVerifyTokenView,
    CustomRefreshVerifyTokenView,
)

app_name = "login"
urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomRefreshVerifyTokenView.as_view(), name='token_refresh'),
    path('verify/', CustomVerifyTokenView.as_view(), name='token_verify'),
]
