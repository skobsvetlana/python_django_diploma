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
    """
    Класс UserProfileViewset представляет собой набор представлений (ViewSet) для работы с профилями пользователей.
    Он использует ModelViewSet, что позволяет автоматически предоставлять действия для создания,
    извлечения, обновления и удаления профилей пользователей.
    """
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Переопределенный метод, который возвращает профиль текущего пользователя.
        Этот метод используется в методах retrieve и update для получения объекта профиля,
        который нужно обновить.
        """
        return self.request.user.profile


    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Метод для извлечения данных профиля текущего пользователя.
        Он использует get_object_or_404 для поиска профиля по пользователю и возвращает
        данные профиля в формате JSON.
        """
        item = get_object_or_404(self.queryset, user=request.user)
        serializer = self.get_serializer(item)
        return Response(serializer.data)


    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Метод для получения списка всех профилей. В данном случае, он возвращает данные
        всех профилей в формате JSON.
        """
        items = self.get_serializer(self.queryset, many=True).data

        return Response(items)

    def create(self, request, *args, **kwargs):
        """
        Метод для создания нового профиля. Он принимает данные из запроса, валидирует их с
        помощью сериализатора и сохраняет новый профиль в базе данных.
        """
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Метод для обновления профиля текущего пользователя. Он также принимает данные из запроса,
        валидирует их и обновляет профиль в базе данных.
        """
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
    """
    Класс AvatarUpdateViewset предназначен для обновления аватара пользователя.
    Он также использует ModelViewSet и работает с профилями пользователей, но в его методе
    update обрабатываются файлы, отправленные через запрос.
    """
    queryset = Profile.objects.all()
    serializer_class = AvatarUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Метод переопределяется для возвращения объекта профиля текущего пользователя.
        """
        return self.request.user.profile

    def update(self, request: Request, *args, **kwargs) -> Response:
        """
        Метод переопределяется для обработки запросов на обновление аватара.
        Он извлекает файлы из запроса, получает объект профиля текущего пользователя,
        создает экземпляр сериализатора с этим объектом и данными из запроса, проверяет
        валидность данных и сохраняет изменения. В ответе возвращается обновленный объект
        профиля с новым аватаром.
        """
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
    """
    Класс ChangePasswordViewSet позволяет пользователям изменять свой пароль.
    Он использует сериализатор ChangePasswordSerializer для валидации текущего и
    нового пароля и обновляет пароль пользователя в базе данных.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Метод переопределяет стандартный метод update из ModelViewSet для выполнения операции
        изменения пароля. Он выполняет следующие действия:
        - получает данные запроса и валидирует их с помощью сериализатора ChangePasswordSerializer.
        - извлекает текущий и новый пароль из валидированных данных.
        - проверяет, соответствует ли текущий пароль, введенный пользователем,
        текущему паролю пользователя в базе данных. Если пароли не совпадают, возвращается ошибка.
        Если текущий пароль верный, устанавливает новый пароль для пользователя и сохраняет изменения.
        Возвращает ответ с сообщением об успешном обновлении пароля.
        """
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











