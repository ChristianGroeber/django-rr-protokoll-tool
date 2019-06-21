from django.contrib.auth import forms, authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .models import Nachmittag, Team, Programmpunkt, Leiter
from logbuch.models import Logbuch, Aufgabe


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
    if str(request.method) == 'GET':
        team = Team.objects.get(name='Starter')
        starter_leiter = team.leiter.all()
        print(starter_leiter)
        logbuch = team.logbuch
        return render(request, 'tool/edit_team.html', {'team': 'Starter', 'programmpunkte': programmpunkte,
                                                       'team_leiter': starter_leiter, 'logbuch': logbuch})
    get_selected_aufgaben(request, programmpunkte)
    save_programmpunkte(request, programmpunkte)
    new_programmpunkt = save_new_programmpunkt(request, nachmittag_obj)
    if new_programmpunkt:
        get_selected_aufgaben_for_new_programmpunkt(request, new_programmpunkt)
    return redirect('.')


def get_selected_aufgaben(request, programmpunkte):
    form = request.POST

    # for old programmpunkte
    for programmpunkt in programmpunkte:
        selected_aufgaben = []
        for aufgabe in Aufgabe.objects.all():
            if form.get(str(aufgabe.id) + '-' + str(programmpunkt.id)):
                print(aufgabe.id)
                selected_aufgaben.append(aufgabe)
        programmpunkt.logbuch_aufgabe.set(selected_aufgaben)


def get_selected_aufgaben_for_new_programmpunkt(request, programmpunkt):
    form = request.POST

    # for new programmpunkte
    selected_aufgaben = []
    for aufgabe in Aufgabe.objects.all():
        if form.get(str(aufgabe.id)):
            print(aufgabe.id)
            selected_aufgaben.append(aufgabe)
    programmpunkt.logbuch_aufgabe.set(selected_aufgaben)


def save_new_programmpunkt(request, nachmittag):
    form = request.POST
    try:
        a = nachmittag.starter.programmpunkte.create(von=form.get('von'),
                                                     bis=form.get('bis'),
                                                     name=form.get('name'),
                                                     beschreibung=form.get('beschreibung'),
                                                     material=form.get('material'))
        selected_leiter = form.getlist('verantwortlich')
        for leiter in selected_leiter:
            a.verantwortlich.add(Leiter.objects.get(username=leiter))
        print('saved')
        return a
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
        new_name = form.get('name' + prog_str)
        new_verantwortlich = form.getlist('verantwortlich' + prog_str)
        new_beschreibung = form.get('beschreibung' + prog_str)
        new_material = form.get('material' + prog_str)
        if new_von is not programmpunkt.von:
            programmpunkt.von = new_von
        if new_bis is not programmpunkt.bis:
            programmpunkt.bis = new_bis
        if new_name is not programmpunkt.name:
            programmpunkt.name = new_name
        if new_beschreibung is not programmpunkt.beschreibung:
            programmpunkt.beschreibung = new_beschreibung
        if new_material is not programmpunkt.material:
            programmpunkt.material = new_material
        leiter_list = []
        for leiter_str in new_verantwortlich:
            leiter_list.append(Leiter.objects.get(username=leiter_str))
        programmpunkt.verantwortlich.set(leiter_list)
        try:
            programmpunkt.save()
        except IntegrityError:
            print("can't save")


def edit_kundschafter(request, nachmittag):
    nachmittag_obj = Nachmittag.objects.get(datum=nachmittag)
    try:
        programmpunkte = nachmittag_obj.kundschafter.programmpunkte.all().order_by('von')
    except AttributeError:
        pass
    if str(request.method) == 'GET':
        kundschafter_leiter = Team.objects.get(name='Kundschafter').leiter.all()
        print(kundschafter_leiter)
        return render(request, 'tool/edit_team.html', {'team': 'Kundschafter', 'programmpunkte': programmpunkte,
                                                       'team_leiter': kundschafter_leiter})
    save_programmpunkte(request, programmpunkte)
    save_new_programmpunkt(request, nachmittag_obj)
    return redirect('.')


def edit_pfadfinder(request, nachmittag):
    nachmittag_obj = Nachmittag.objects.get(datum=nachmittag)
    try:
        programmpunkte = nachmittag_obj.starter.programmpunkte.all().order_by('von')
    except AttributeError:
        pass
    if str(request.method) == 'GET':
        pfadfinder_leiter = Team.objects.get(name='Pfadfinder').leiter.all()
        print(pfadfinder_leiter)
        return render(request, 'tool/edit_team.html', {'team': 'Pfadfinder', 'programmpunkte': programmpunkte,
                                                       'team_leiter': pfadfinder_leiter})
    save_programmpunkte(request, programmpunkte)
    save_new_programmpunkt(request, nachmittag_obj)
    return redirect('.')


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
