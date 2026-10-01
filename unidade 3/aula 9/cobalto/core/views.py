from django.contrib import messages
from django.shortcuts import redirect, render

from .content import CASES, MARCOS, PROCESSO, SOLUCOES, TIME, VALORES
from .forms import ContatoForm


def home(request):
    return render(request, "core/home.html", {
        "solucoes": SOLUCOES,
        "processo": PROCESSO,
        "cases": CASES,
    })


def sobre(request):
    return render(request, "core/sobre.html", {
        "valores": VALORES,
        "marcos": MARCOS,
        "time": TIME,
    })


def solucoes(request):
    return render(request, "core/solucoes.html", {
        "solucoes": SOLUCOES,
        "processo": PROCESSO,
    })


def contato(request):
    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recebemos sua mensagem. Respondemos em até 1 dia útil.")
            return redirect("core:contato")
    else:
        assunto = request.GET.get("assunto")
        form = ContatoForm(initial={"assunto": assunto} if assunto else None)
    return render(request, "core/contato.html", {"form": form})
