from django.db import models

# Create your models here.

class Solucao(models.Model):
    titulo = models.CharField(max_length=60)
    descricao = models.TextField()
    preco = models.DecimalField(decimal_places=2, max_digits=10)
    disponibilidade = models.BooleanField(default=True)
    image_url = models.URLField()