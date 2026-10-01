from django.test import TestCase
from django.urls import reverse

from .models import Contato


class PaginasTests(TestCase):
    def test_paginas_publicas_respondem(self):
        for nome in ("home", "sobre", "solucoes", "contato"):
            with self.subTest(pagina=nome):
                resposta = self.client.get(reverse(f"core:{nome}"))
                self.assertEqual(resposta.status_code, 200)

    def test_contato_salva_mensagem(self):
        resposta = self.client.post(reverse("core:contato"), {
            "nome": "Ana Souza",
            "email": "ana@exemplo.com.br",
            "empresa": "Exemplo Ltda",
            "assunto": "projeto",
            "mensagem": "Preciso de um sistema de pedidos.",
        }, follow=True)
        self.assertRedirects(resposta, reverse("core:contato"))
        self.assertEqual(Contato.objects.count(), 1)
        self.assertContains(resposta, "Recebemos sua mensagem")

    def test_contato_invalido_mostra_erros(self):
        resposta = self.client.post(reverse("core:contato"), {"nome": "", "email": "x"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Contato.objects.count(), 0)
        self.assertContains(resposta, "campo__erro")
