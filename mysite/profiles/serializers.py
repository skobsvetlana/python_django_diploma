from django.contrib.auth.models import User

from profiles.models import Profile

from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    fullName =serializers.SerializerMethodField(method_name="get_fullName")
    email = serializers.EmailField(source='user.email', required=True)

    class Meta:
        model = Profile
        fields = [
            "fullName",
            "email",
            "phone",
            "avatar",
        ]

    def get_fullName(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"





