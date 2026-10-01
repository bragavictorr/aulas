from django.shortcuts import render
from .models import Solucao

def home(request):
    return render (request, 'home.html')

def solucoes(request):
    return render (request, 'solucoes.html')

def sobre(request):
    return render (request, 'sobre.html')

def login(request):
    return render (request, 'login.html')


def solucoes(request):
    lista_solucoes = Solucao.objects.all()
    return render(request, 'solucoes.html',{'lista_solucoes': lista_solucoes})
