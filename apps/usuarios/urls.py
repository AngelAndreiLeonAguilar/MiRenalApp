from django.urls import path
from . import views

urlpatterns = [
    # Otras rutas
    path('perfil/', views.perfil_usuario, name='perfil'), 
]