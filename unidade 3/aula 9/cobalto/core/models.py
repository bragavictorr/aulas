from django.db import models


class Contato(models.Model):
    ASSUNTOS = [
        ("projeto", "Quero iniciar um projeto"),
        ("squad", "Quero montar um squad"),
        ("legado", "Tenho um sistema antigo para modernizar"),
        ("outro", "Outro assunto"),
    ]

    nome = models.CharField("nome", max_length=120)
    email = models.EmailField("e-mail")
    empresa = models.CharField("empresa", max_length=120, blank=True)
    assunto = models.CharField("assunto", max_length=20, choices=ASSUNTOS, default="projeto")
    mensagem = models.TextField("mensagem")
    criado_em = models.DateTimeField("recebido em", auto_now_add=True)
    respondido = models.BooleanField("respondido", default=False)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "contato"
        verbose_name_plural = "contatos"

    def __str__(self):
        return f"{self.nome} ({self.get_assunto_display()})"
