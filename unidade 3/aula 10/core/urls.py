
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('login/', views.login, name='login'),
    path('contato/', views.contato, name='contato'),
    path('lead/', views.lead, name='lead'),
]