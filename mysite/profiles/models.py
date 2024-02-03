from django.db import models
from django.contrib.auth.models import User

def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "images/profiles/user_{pk}/avatar/{filename}".format(
        pk=instance.user.pk,
        filename=filename
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    src = models.ImageField(
        default="pics/daisy.jpeg",
        upload_to=profile_avatar_directory_path,
        null=True,
        blank=True,
        verbose_name='avatar'
    )
    alt = models.CharField(max_length=200, null=False, blank=True)

    # class Meta:
    #     permissions = (("change_avatar", "can change avatar of profile"),)

    def __str__(self):
        return self.user.username

    @property
    def avatar(self):
        return {'src': self.src,
                'alt': self.alt,
                }



