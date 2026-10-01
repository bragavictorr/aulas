from django import forms

from .models import Contato


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ["nome", "email", "empresa", "assunto", "mensagem"]
        widgets = {
            "nome": forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Como podemos te chamar?"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "voce@empresa.com.br"}),
            "empresa": forms.TextInput(attrs={"autocomplete": "organization", "placeholder": "Opcional"}),
            "mensagem": forms.Textarea(attrs={"rows": 5, "placeholder": "Conte o que você precisa resolver. Pode ser em poucas linhas."}),
        }
