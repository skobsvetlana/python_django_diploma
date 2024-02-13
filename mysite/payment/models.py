from django.db import models

class Payment(models.Model):
    number = models.CharField(null=False, max_length=16)
    name = models.CharField(max_length=100)
    month = models.CharField(null=False, max_length=2)
    year = models.CharField(null=False, max_length=4)
    code = models.CharField(null=False, max_length=3)

    def __str__(self):
        return (f"name: {self.name}   "
                f"number: {self.number}   "
                f"month/year {self.month}/{self.year} code: {self.code}")

