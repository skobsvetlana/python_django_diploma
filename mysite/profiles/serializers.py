from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from profiles.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
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
        Update and return an existing `Profile` instance, given the validated data.
        """
        instance.user.first_name = validated_data['user']['first_name']
        instance.user.email = validated_data['user']['email']
        instance.user.save()
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class AvatarUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source="src")

    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]

    def update(self, instance, validated_data):
        """
        Update and return an existing `Profile` instance, given the validated data.
        """
        instance.src = validated_data.get('src', instance.src)
        instance.save()
        return instance



