from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Profile.
    """
    queryset = User.objects.all()
    username = serializers.CharField(
        source='user.username',
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )
    fullName = serializers.CharField(source="user.first_name", required=True)
    email = serializers.EmailField(
        source='user.email',
        required=True,
        validators=[UniqueValidator(queryset=queryset)]
    )
    phone = serializers.CharField(required=True)
    avatar = serializers.DictField(required=False)

    class Meta:
        model = Profile
        fields = [
            "username",
            "fullName",
            "email",
            "phone",
            "avatar",
        ]


    def update(self, instance, validated_data):
        """
        Обновляет существующий экземпляр класса Profile на основе переданных данных.
        Он обновляет имя пользователя, электронную почту, телефон и аватар.
        """
        instance.user.first_name = validated_data['user']['first_name']
        instance.user.email = validated_data['user']['email']
        instance.user.save()
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class AvatarUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления аватара пользователя.
    """
    avatar = serializers.ImageField(source="src")

    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]

    def update(self, instance, validated_data):
        """
        Переопределяет стандартный метод update для обновления экземпляра модели Profile на
        основе валидированных данных.
        """
        instance.src = validated_data.get('src', instance.src)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор для изменения пароля пользователя.
    """
    currentPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)
    # confirmNewPassword = serializers.CharField(required=True)

    # def validate(self, data):
    #     if data['newPassword'] != data['confirmNewPassword']:
    #         raise serializers.ValidationError("New passwords not match.")
    #     return data



