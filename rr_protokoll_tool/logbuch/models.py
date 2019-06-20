from django.db import models
from django.db.models import ImageField
# Create your models here.


class Aufgabe(models.Model):
    beschreibung = models.CharField(max_length=500)

    def __str__(self):
        return self.beschreibung


class UnterThema(models.Model):
    name = models.CharField(max_length=100)
    anmerkung = models.CharField(max_length=200, blank=True)
    aufgaben = models.ManyToManyField(Aufgabe, blank=True)

    def __str__(self):
        return self.name


class Thema(models.Model):
    name = models.CharField(max_length=100)
    unterthemen = models.ManyToManyField(UnterThema, blank=True)

    def __str__(self):
        return self.name


class Abzeichen(models.Model):
    name = models.CharField(max_length=100)
    beschreibung = models.CharField(max_length=500, blank=True)
    abbildung = ImageField(upload_to='abzeichen', blank=True)
    themen = models.ManyToManyField(Thema, blank=True)

    def __str__(self):
        return self.name


class Logbuch(models.Model):
    abzeichen = models.ManyToManyField(Abzeichen, blank=True)
