from django.shortcuts import render
from .tasks import calculate_rang
# Create your views here.

def login(request):
    return render(request, 'userauth/login.html')

def calc_rang(request):
    calculate_rang.delay()