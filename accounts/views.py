from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm
    return render(request, 'login.html', {'form': form})


def user_registration(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'registration.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'Successfully logged out')
    return redirect('home')
