from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')
