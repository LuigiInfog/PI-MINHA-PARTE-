from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('casosbase/', views.casosbase, name='casosbase'),
    path('forum/', views.forum, name='forum'),
    path('login/', views.login_view, name='login'),
    path('investigar/', views.investigar, name='investigar'),
    path('investigacoes/', views.investigacoes, name='investigacoes'),
    path('investigacoes/nova/', views.nova_investigacao, name='nova_investigacao'),
    path('investigacoes/<int:id>/', views.relatorio_investigacao, name='relatorio_investigacao'),
    path('investigacoes/<int:id>/pdf/', views.relatorio_investigacao_pdf, name='relatorio_investigacao_pdf'),
]