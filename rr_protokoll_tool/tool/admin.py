from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomLeiterCreationForm, CustomLeiterChangeForm
from .models import Leiter, Kind, Team, Kurs, TeamProgramm, Nachmittag, Programmpunkt


class CustomLeiterAdmin(UserAdmin):
    add_form = CustomLeiterCreationForm
    form = CustomLeiterChangeForm
    model = Leiter
    list_display = ['email', 'username', ]


admin.site.register(Leiter, CustomLeiterAdmin)
admin.site.register(Kurs)
admin.site.register(Team)
admin.site.register(Kind)
admin.site.register(TeamProgramm)
admin.site.register(Nachmittag)
admin.site.register(Programmpunkt)
