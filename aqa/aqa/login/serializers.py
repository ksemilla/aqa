from rest_framework import serializers

import jwt

from config import settings

from aqa.users.serializers import UserSerializer
from aqa.users.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        # data.update({'user': self.user.username})
        data.update({'user': {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'name': self.user.name,
            'scope': self.user.scope

        }})
        # data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data

class CustomVerifyTokenSerializer(TokenVerifySerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomVerifyTokenSerializer, self).validate(attrs)

        # data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data

class CustomRefreshTokenSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)
        decoded = jwt.decode(data['access'], settings.SECRET_KEY)
        user = User.objects.get(id=decoded['user_id'])
        data['user'] = UserSerializer(user).data
        return data