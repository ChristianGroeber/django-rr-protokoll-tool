from django.db import models
from django.db.models import ImageField
# Create your models here.


class Abzeichen(models.Model):
    name = models.CharField(max_length=100)
    beschreibung = models.CharField(max_length=500, blank=True)
    abbildung = ImageField(upload_to='abzeichen', blank=True)

    def __str__(self):
        return self.name


class Thema(models.Model):
    name = models.CharField(max_length=100)
    gehoert_zu_abzeichen = models.ForeignKey(Abzeichen, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UnterThema(models.Model):
    name = models.CharField(max_length=100)
    anmerkung = models.CharField(max_length=200, blank=True)
    gehoert_zu = models.ForeignKey(Thema, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Aufgabe(models.Model):
    beschreibung = models.CharField(max_length=500)
    gehoert_zu_thema = models.ForeignKey(Thema, on_delete=models.SET_NULL, null=True, blank=True)
    gehoert_zu_unter_thema = models.ForeignKey(UnterThema, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.beschreibung


class Logbuch(models.Model):
    aufgaben = models.ManyToManyField(Aufgabe, blank=True)
