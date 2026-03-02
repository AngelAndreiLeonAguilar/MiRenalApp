from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'style': 'height: 50px; line-height: 50px;',  # altura fija y alineación
            'placeholder': 'Usuario',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'style': 'height: 50px; line-height: 50px;',  # altura fija y alineación
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password'
        })
    )