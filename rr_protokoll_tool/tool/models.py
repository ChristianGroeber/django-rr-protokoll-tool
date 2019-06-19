from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Leiter(AbstractUser):
    geburtstag = models.DateField(null=True, blank=True)
    test = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return 'Leiter'