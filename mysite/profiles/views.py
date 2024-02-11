from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from profiles.serializers import (
    ProfileSerializer,
    AvatarUpdateSerializer,
)
from profiles.models import Profile


class UserProfileViewset(ModelViewSet):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        item = get_object_or_404(self.queryset, user=request.user)
        serializer = self.get_serializer(item)
        print("++++++++++++++++++++++++profile_retrieve")
        return Response(serializer.data)


    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)

    def create(self, request, *args, **kwargs):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!create profile view")
        data = request.data
        print(data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


    def update(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        instance = self.get_object()
        print("+++++++++update profile")
        print(data)
        serializer = self.get_serializer(
            instance,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


class AvatarUpdateViewset(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = AvatarUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def update(self, request: Request, *args, **kwargs) -> Response:
        data = request.FILES
        print("avatar data", data)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance,
            data=data,
        )
        serializer.is_valid(raise_exception=True)
        print("update avatar ", serializer.validated_data)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )




# def update(self, request: Request, *args, **kwargs) -> Response:
    #     avatar = request.data["avatar"]
    #     email = request.data["email"]
    #     phone = request.data["phone"]
    #     first_name, last_name = (request.data['fullName'].split(" "))
    #
    #     user = request.user
    #     profile, created = Profile.objects.get_or_create(user=user)
    #
    #     profile.user.first_name = first_name
    #     profile.user.last_name = last_name
    #     profile.user.email = email
    #     profile.phone = phone
    #
    #     # if avatar:
    #     #     profile.avatar = avatar
    #
    #     profile.save()
    #
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!profile_update")
    #
    #     serializer = self.get_serializer(profile)
    #     item = serializer.data
    #     print(item)
    #     return Response(item, status=status.HTTP_200_OK)






