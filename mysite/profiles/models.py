from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    """
    Определяет путь к директории для хранения аватара пользователя в профиле.

    Параметры:
    - instance: Экземпляр модели Profile, для которого загружается аватар.
    - filename: Имя файла аватара, который загружается.

    Возвращает:
    Строку, представляющую путь к директории, где будет храниться аватар.
    Путь формируется как "profiles/user_{pk}/avatar/{filename}", где {pk} - это первичный ключ пользователя,
    а {filename} - имя загружаемого файла.
    """
    return "profiles/user_{pk}/avatar/{filename}".format(
        pk=instance.user.pk,
        filename=filename
    )


class Profile(models.Model):
    """
    Класс Profile представляет собой модель, которая связана с моделью User через однонаправленную связь
    OneToOneField.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    src = models.ImageField(
        # default="pics/avatar.jpg",
        upload_to=profile_avatar_directory_path,
        null=True,
        blank=True,
        verbose_name='avatar'
    )
    alt = models.CharField(max_length=200, null=True, blank=True, default="")

    @property
    def avatar(self):
        """
        Возвращает словарь с информацией об аватаре пользователя, если изображение аватара (src) существует.
        """
        if self.src:
            return {
                "src": serializers.ImageField().to_representation(self.src),
                "alt": self.alt
            }
        return None

    def __str__(self):
        return self.user.username
