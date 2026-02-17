from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS_USUARIO = [
        ('paciente', 'Paciente'),
        ('medico', 'Médico'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS_USUARIO, default='paciente')

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"