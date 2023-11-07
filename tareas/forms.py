from django import forms
from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'importante']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripción'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto mb-3'}),
        }
