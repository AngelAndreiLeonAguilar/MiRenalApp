from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    TIPOS_USUARIO = [
        ('paciente', 'Paciente'),
        ('medico', 'Médico'),
    ]
    # Usamos 'user' para mantener consistencia con tu código previo
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=10, choices=TIPOS_USUARIO, default='paciente')
    # Nuevo campo para el sistema de moderación
    esta_bloqueado = models.BooleanField(default=False) 
    # NUEVO: Campo para la foto de perfil
    imagen = models.ImageField(upload_to='perfiles/', default='perfiles/default.png', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"

# --- SEÑALES PARA CREACIÓN AUTOMÁTICA ---
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Esto crea el perfil automáticamente cuando creas un usuario o superusuario
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()