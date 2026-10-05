from django.shortcuts import render
from .models import Cliente

# Create your views here.
def home(request):
    lista_cliente = Cliente.objects.all()


    total_cliente = 0
    for cliente in lista_cliente:
        total_cliente += 1
              
    fechado= 0
    for cliente in lista_cliente:
        if cliente.status == 'fechado':
            fechado += 1

    total_negociacao = 0
    for cliente in lista_cliente:
        if cliente.status == 'negociacao':
            total_negociacao += 1


    valor_total = 0
    for cliente in lista_cliente:
     valor_total += cliente.valor_proposta
        
   
    contexto = {
        'lista_cliente': lista_cliente,
        'total_negociacao': total_negociacao,
        'fechado': fechado,
        'total_cliente' : total_cliente,
        'valor_total' : valor_total
    }

   
    return render(request,'home.html', context=contexto)

