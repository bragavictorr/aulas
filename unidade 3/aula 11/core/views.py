from django.shortcuts import render
import requests 

# Create your views here.
def home(request):
    resposta = {}
    if request.method == 'POST':
        cep_usuario = request.POST.get('cep')
        resposta = requests.get(f"https://viacep.com.br/ws/{cep_usuario}/json/").json()

        
    
    return render(request, 'home.html', context={'resposta': resposta})