# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('casosbase/', views.casosbase, name='casosbase'),
    path('forum/', views.forum, name='forum'),
    path('login/', views.login_view, name='login'),
    path('investigar/', views.investigar, name='investigar'),
    path('investigacoes/', views.investigacoes, name='investigacoes'),
    path('nova_investigacao/', views.nova_investigacao, name='nova_investigacao'),
    path('relatorio/<int:id>/', views.relatorio_investigacao, name='relatorio_investigacao'),
    path('relatorio/<int:id>/pdf/', views.relatorio_investigacao_pdf, name='relatorio_investigacao_pdf'),
]