from django.db import models
from django.contrib.auth.models import User

class Pacientes(models.Model):
    # Relación con el usuario que se loguea en el sistema
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # Campos de registro diario
    peso = models.CharField(max_length=10)          # Ejemplo: "70 kg"
    presion = models.CharField(max_length=10)       # Ejemplo: "120/80"
    liquidos = models.CharField(max_length=10)      # Ejemplo: "1.5 L"
    sintomas = models.TextField(blank=True, null=True)  # Texto libre

    # Fecha automática de creación del registro
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
class EvaluacionNutricional(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    peso = models.FloatField() # kg [cite: 7]
    talla = models.FloatField() # m [cite: 6]
    imc = models.FloatField() # Peso / Talla² 
    tipo_paciente = models.CharField(max_length=50) # Conservador, Hemodiálisis, etc. [cite: 8-12]