from django.contrib import admin

# Register your models here.
from django import forms

class CasoDeEstudoForm(forms.ModelForm):
    class Meta:
        fields = ['titulo', 'descricao', 'data', 'categoria']
