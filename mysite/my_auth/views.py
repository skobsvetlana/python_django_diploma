import json

from django.contrib.auth import login, logout, authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from my_auth.serializers import UserRegistrationSerializer

class LoginViewSet(viewsets.GenericViewSet):
    """
    Осуществляет аутентификацию и логин пользователя.
    """
    def create(self, request, *args, **kwargs):
        data = json.loads(next(iter(request.data.keys())))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!user_login")
        print(data.get('username'), data.get('password'))

        user = authenticate(
            self.request,
            username=data.get('username'),
            password=data.get('password'),
        )

        if user:
            login(request=request, user=user)
            return Response(
                data={"detail": "Login successful."},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                data={"detail": "Invalid login credentials."},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutViewSet(viewsets.GenericViewSet):
    """
    Вызовает стандартный метод logout Django, который очищает сессию пользователя
    """

    def update(self, request, *args, **kwargs):
        # Вызов стандартного метода logout Django, который очищает сессию пользователя
        logout(request)
        return Response(
            data={"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )


class UserRegistrationViewSet(viewsets.GenericViewSet):
    """
    Creates a new user, authenticates and logs him in.
    """

    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!user_registration")
        data = json.loads(next(iter(request.data.keys())))
        print(data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        user = serializer.save()
        print('cat', user.username, user.password)
        user = authenticate(
            request,
            username=user.username,
            password=data.get('password'))

        if user:
            login(request=request, user=user)
            return Response(
                data={"detail": "User registered and logged in successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                data={"detail": "Unable to log in after registration."},
                status=status.HTTP_400_BAD_REQUEST,
            )

