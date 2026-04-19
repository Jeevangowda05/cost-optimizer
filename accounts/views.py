from django.contrib.auth import logout
from django.shortcuts import redirect, render


def signup_view(request):
    return render(request, 'signup.html')


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('dashboard:index')
