from django import forms
from .models import Pacientes

class PacientesForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ["peso", "presion", "liquidos", "sintomas"]
        widgets = {
            "peso": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 70 kg"}),
            "presion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 120/80"}),
            "liquidos": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 1.5 L"}),
            "sintomas": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Describe tus síntomas"}),
        }