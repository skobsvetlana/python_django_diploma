from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from profiles.models import Profile




class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=True)
    fullName = serializers.SerializerMethodField(method_name="get_fullName")
    email = serializers.EmailField(
        source='user.email',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone = serializers.CharField(required=True)
    avatar = serializers.DictField(required=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "fullName",
            "email",
            "phone",
            "avatar",
        ]

    def get_fullName(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

