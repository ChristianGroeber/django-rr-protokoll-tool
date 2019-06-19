from django.contrib.auth import forms, authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Nachmittag, Team
from logbuch.models import Logbuch


# Create your views here.


def index(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    return render(request, 'tool/index.html')


def jahresplan(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    nachmittage = Nachmittag.objects.all()
    return render(request, 'tool/jahresplan.html', {'nachmittage': nachmittage})


def nachmittag(request, nachmittag):
    nachmittag_obj = Nachmittag.objects.get(datum=nachmittag)
    return render(request, 'tool/nachmittag.html', {'nachmittag': nachmittag_obj})


def edit_starter(request, nachmittag):
    nachmittag_obj = Nachmittag.objects.get(datum=nachmittag)
    # aufgaben = Team.objects.objects.get(name='Starter')
    return render(request, 'tool/edit_team.html', {'team': 'Starter'})


def edit_kundschafter(request, nachmittag):
    nachmittag_obj = Nachmittag.objects.get(datum=nachmittag)
    return render(request, 'tool/edit_team.html', {'team': 'Kundschafter'})


def edit_pfadfinder(request, nachmittag):
    nachmittag_obj = Nachmittag.objects.get(datum=nachmittag)
    return render(request, 'tool/edit_team.html', {'team': 'Pfadfinder'})


def user_login(request):
    if str(request.user) is not 'AnonymousUser':
        return redirect('home')
    form = forms.AuthenticationForm(request.POST or None)
    if request.method == 'GET':
        return render(request, 'tool/login.html', {'form': form})
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('login')