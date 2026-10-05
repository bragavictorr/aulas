from django.db import models

# Create your models here.
class Cliente (models.Model):
    STATUS_CHOICES = [
        ('negociacao', 'Em Negociaoção'),
        ('fechado','Fechado'),
        ('perdido', 'Perdido'),
    ]




    nome = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    telefone = models.CharField(max_length=20)
    valor_proposta = models.DecimalField(max_digits=10, decimal_places=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='negociacao')

    def __str__(self):
        return self.nome
    