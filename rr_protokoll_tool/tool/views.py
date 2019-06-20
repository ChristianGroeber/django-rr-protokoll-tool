from django.contrib.auth import forms, authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Nachmittag, Team, Programmpunkt
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
    try:
        programmpunkte = nachmittag_obj.starter.programmpunkte.all().order_by('von')
    except AttributeError:
        pass
    print(programmpunkte)
    if str(request.method) == 'GET':
        return render(request, 'tool/edit_team.html', {'team': 'Starter', 'programmpunkte': programmpunkte})
    save_programmpunkte(request, programmpunkte)
    save_new_programmpunkt(request, nachmittag_obj)
    return redirect('.')


def save_new_programmpunkt(request, nachmittag):
    form = request.POST
    try:
        nachmittag.starter.programmpunkte.create(von=form.get('von'), bis=form.get('bis'))
        print('saved')
    except ValueError:
        print("didn't save")
    except IntegrityError:
        print("Integrity Error")


def save_programmpunkte(request, programmpunkte):
    for programmpunkt in programmpunkte:
        prog_str = str(programmpunkt.id)
        form = request.POST
        new_von = form.get('von' + prog_str)
        new_bis = form.get('bis' + prog_str)
        if new_von is not programmpunkt.von:
            programmpunkt.von = new_von
        if new_bis is not programmpunkt.bis:
            programmpunkt.bis = new_bis
        try:
            programmpunkt.save()
        except IntegrityError:
            print("can't save")


def edit_kundschafter(request, nachmittag):
    nachmittag_obj = Nachmittag.objects.get(datum=nachmittag)
    return render(request, 'tool/edit_team.html', {'team': 'Kundschafter'})


def edit_pfadfinder(request, nachmittag):
    nachmittag_obj = Nachmittag.objects.get(datum=nachmittag)
    return render(request, 'tool/edit_team.html', {'team': 'Pfadfinder'})


def delete_starter(request, nachmittag, programmpunkt):
    Programmpunkt.objects.filter(id=programmpunkt).delete()
    return redirect('../../')


def delete_kundschafter(request, nachmittag, programmpunkt):
    Programmpunkt.objects.filter(id=programmpunkt).delete()
    return redirect('../../')


def delete_pfadfinder(request, nachmittag, programmpunkt):
    Programmpunkt.objects.filter(id=programmpunkt).delete()
    return redirect('../../')


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