from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    name = serializers.CharField(source="first_name")
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "password",
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Создает нового пользователя с данными из validated_data.
        """
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user










