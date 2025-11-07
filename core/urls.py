# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('resultados/', views.resultados, name='resultados'),
    path('historico/', views.historico, name='historico'),
    path('contato/', views.contato, name='contato'),
]
