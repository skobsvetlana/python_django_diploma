from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from profiles.serializers import (
    ProfileSerializer,
    AvatarUpdateSerializer,
    ChangePasswordSerializer,
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
        return Response(serializer.data)


    def list(self, request: Request, *args, **kwargs) -> Response:
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


    def update(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
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
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance,
            data=data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


class ChangePasswordViewSet(ModelViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        currentPassword = serializer.validated_data.get('currentPassword')
        newPassword = serializer.validated_data.get('newPassword')

        if not request.user.check_password(currentPassword):
            print("Wrong password.")
            return Response(
                data={"currentPassword": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.set_password(newPassword)
        request.user.save()

        return Response(
            data={"message": "Password updated successfully."},
            status=status.HTTP_200_OK
        )











