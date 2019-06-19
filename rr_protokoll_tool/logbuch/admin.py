from django.contrib import admin

# Register your models here.

from .models import Logbuch, Abzeichen, Aufgabe, Thema, UnterThema

admin.site.register(Logbuch)
admin.site.register(Abzeichen)
admin.site.register(Aufgabe)
admin.site.register(Thema)
admin.site.register(UnterThema)
