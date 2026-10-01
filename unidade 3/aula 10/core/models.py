from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    image_url = models.URLField(max_length=500)

class Mensagem(models.Model):
    texto_mensagem = models.TextField()
    data_criaçao = models.DateTimeField(auto_now=True)
  
class Lead(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField( max_length=254)
    interesse = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)