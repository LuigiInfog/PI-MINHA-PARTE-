# app/models.py
from django.db import models

class Investigacao(models.Model):
    titulo = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)
    descricao = models.TextField()
    
    # Novos campos para o sistema de relacionamento
    localizacao = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.titulo