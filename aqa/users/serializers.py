from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username','name', 'scope', 'fullname', 'first_name', 'last_name', \
            'is_active',
        )

    def __str__():
        return UserSerializer.username