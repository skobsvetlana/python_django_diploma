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

    # def get_split_fullName(self, name):
    #     splited_name = name.split(" ")
    #     len_name = len(splited_name)
    #     if len_name > 1:
    #         first_name = " ".join(splited_name[:len_name - 1])
    #         last_name = splited_name[len_name - 1]
    #     else:
    #         first_name = name
    #         last_name = ""
    #
    #     return first_name, last_name


    # def create(self, validated_data):
    #     """
    #     Create and return a new `Profile` instance, given the validated data.
    #     """
    #     name = validated_data["fullName"]
    #     first_name, last_name = self.get_split_fullName(name)
    #
    #     pofile = Profile.objects.create(
    #         first_name=first_name,
    #         last_name=last_name,
    #         username=validated_data["username"],
    #     )
    #
    #     return pofile

    def update(self, instance, validated_data):
        """
        Update and return an existing `Profile` instance, given the validated data.
        """
        print("++++++++++++++profile update")
        print("validated_data", validated_data)
        instance.user.first_name = validated_data.get('fullName', instance.user.first_name)
        instance.src = validated_data['avatar']['src']
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


