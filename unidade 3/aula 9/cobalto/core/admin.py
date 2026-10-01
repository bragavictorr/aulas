from django.contrib import admin

from .models import Contato


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "empresa", "assunto", "criado_em", "respondido")
    list_filter = ("assunto", "respondido", "criado_em")
    search_fields = ("nome", "email", "empresa", "mensagem")
    list_editable = ("respondido",)
    readonly_fields = ("criado_em",)
