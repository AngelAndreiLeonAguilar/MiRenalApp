from django.db import models
from django.contrib.auth.models import User

class Opinion(models.Model):
    # Relacionamos con el usuario (como 'Nol') que ya tienes en la DB
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=500)
    # Calificación de 1 a 5
    estrellas = models.PositiveSmallIntegerField(default=5)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Sistema de votos
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='blog_dislikes', blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.estrellas} estrellas"