from django.contrib import admin
from .models import Produto
from .models import Mensagem
from .models import Lead


# Register your models here.
admin.site.register(Produto)
admin.site.register(Mensagem)
admin.site.register(Lead)