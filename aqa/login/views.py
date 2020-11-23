import jwt
import copy

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from config import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .serializers import CustomTokenObtainPairSerializer, CustomVerifyTokenSerializer, CustomRefreshTokenSerializer
from aqa.users.models import User
from aqa.users.serializers import UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer

class CustomVerifyTokenView(TokenVerifyView):
    serializer_class = CustomVerifyTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            data = copy.deepcopy(request.data)
            decoded = jwt.decode(data['token'], settings.local.SECRET_KEY)
            user = User.objects.get(id=decoded['user_id'])
        except TokenError as e:
            raise InvalidToken(e.args[0])

        temp_data = serializer.validated_data
        temp_data['user'] = UserSerializer(user).data

        return Response(temp_data, status=status.HTTP_200_OK)

class CustomRefreshVerifyTokenView(TokenRefreshView):
    serializer_class = CustomRefreshTokenSerializer