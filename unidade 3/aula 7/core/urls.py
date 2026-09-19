
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name="home"),
    path('sobre', views.sobre, name="sobre"),
    path('contato',views.contato, name="contato"),
    path('', views.inicio, name='inicio'),
]
