from django.contrib.auth import forms, authenticate, login, logout
from django.shortcuts import render, redirect


# Create your views here.


def index(request):
    if str(request.user) is 'AnonymousUser':
        return redirect('login')
    return render(request, 'tool/index.html')


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
    logout(request.user)
    return redirect('login')
