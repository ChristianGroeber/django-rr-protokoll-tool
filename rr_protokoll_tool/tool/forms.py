from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Leiter


class CustomLeiterCreationForm(UserCreationForm.Meta):

    class Meta(UserCreationForm):
        model = Leiter
        fields = ('username', 'email')


class CustomLeiterChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Leiter
        fields = ('username', 'email')
