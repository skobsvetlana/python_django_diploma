from django.db import models

class Specification(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}    {self.value}'