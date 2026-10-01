from django.contrib import admin
from django.urls import path
from webcore import views

urlpatterns = [
    path('', views.home, name='home'),
    path('solucoes/', views.solucoes, name='solucoes'),
    path('sobre/', views.sobre, name='sobre'),
    path('login/', views.login, name='login')

]
