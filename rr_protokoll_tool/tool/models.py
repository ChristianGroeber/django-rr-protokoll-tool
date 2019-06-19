from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import ImageField

from logbuch.models import Aufgabe, Logbuch, Abzeichen


class Kurs(models.Model):
    name = models.CharField(max_length=100)
    mindestalter = models.IntegerField()

    def __str__(self):
        return self.name


class Leiter(AbstractUser):
    geburtstag = models.DateField(null=True, blank=True)
    besuchte_kurse = models.ManyToManyField(Kurs, blank=True)
    dabei_seit = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Leiter'


class Kind(models.Model):
    name = models.CharField(max_length=100)
    vorname = models.CharField(max_length=100)
    geburtstag = models.DateField()
    bild = ImageField(upload_to='kinder/', blank=True)
    erhaltene_abzeichen = models.ManyToManyField(Abzeichen, blank=True)

    def __str__(self):
        return self.vorname


class Team(models.Model):
    name = models.CharField(max_length=100)
    leiter = models.ManyToManyField(Leiter, blank=True)
    kinder = models.ManyToManyField(Kind, blank=True)
    logbuch = models.OneToOneField(Logbuch, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class TeamProgramm(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    logbuch_aufgaben = models.ManyToManyField(Aufgabe, blank=True)


class Nachmittag(models.Model):
    datum = models.DateField()
    starter = models.ForeignKey(TeamProgramm, on_delete=models.SET_NULL, null=True, blank=True, related_name='Starter')
    kundschafter = models.ForeignKey(TeamProgramm, on_delete=models.SET_NULL, null=True, blank=True, related_name='Kundschafter')
    pfadfinder = models.ForeignKey(TeamProgramm, on_delete=models.SET_NULL, null=True, blank=True, related_name='Pfadfinder')

    def __str__(self):
        return str(self.datum)
