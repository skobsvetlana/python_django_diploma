from django.db import models

class Tag(models.Model):
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f'{self.name}'