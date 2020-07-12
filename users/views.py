from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm

def register_view(request):

    form = RegisterForm(request.POST or None)
    next = request.GET['next'] if 'next' in request.GET else '/games'

    if form.is_valid():
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        user = authenticate(username=user.username, password=password)
        login(request, user)
        return redirect(next)

    return render(request, 'users/register.html', {
        'form': form,
        'next': request.GET['next'] if 'next' in request.GET else '/games'
    })

def login_view(request):

    form = LoginForm(request.POST or None)
    next = request.GET['next'] if 'next' in request.GET else '/games'

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(next)

    return render(request, 'users/login.html', {
        'form': form,
        'next': next
    })
