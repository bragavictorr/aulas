from django.shortcuts import render
from .models import Produto
from .models import Mensagem
from .models import Lead

# Create your views here.

def sobre(request):
    return render(request, 'sobre.html')

def login(request):
    return render(request, 'login.html')

def home(request):
    produtos = Produto.objects.all()
    contexto = { 'produtos':produtos,}
    return render(request, 'home.html', contexto)

def contato(request):
    if request.method == 'POST':
        mensagem_usuario = request.POST.get('mensagem')
        Mensagem.objects.create(texto_mensagem=mensagem_usuario)
        
    return render(request, 'contato.html')

def lead(request):
    if request.method == 'POST':
        nome_Lead = request.POST.get('nome')
        email_Lead = request.POST.get('email')
        produto_id = request.POST.get('interesse')


        Produto_selecionado = Produto.objects.get(id=produto_id)
        Lead.objects.create(
            nome = nome_Lead,
            email = email_Lead,
            interesse = Produto_selecionado
        )

    produtos = Produto.objects.all()
    contexto = {'produtos': produtos}
        
    return render(request, 'lead.html', contexto)



