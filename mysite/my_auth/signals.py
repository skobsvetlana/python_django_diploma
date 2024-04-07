from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from profiles.models import Profile


# Функция создает профиль пользователя после его создания.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Функция сохраняет профиль пользователя после каждого сохранения пользователя.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()