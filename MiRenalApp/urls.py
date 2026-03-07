from django.contrib import admin
from django.urls import path
from apps.usuarios import views as usuarios_views
from django.contrib.auth import views as auth_views
from apps.blog import views as blog_views 

urlpatterns = [
    # Admin (siempre arriba)
    path('admin/', admin.site.urls),

    # Rutas del Foro (Ponlas arriba para que tengan prioridad)
    path('foro/', blog_views.foro, name='foro'),
    path('dar-like/<int:pk>/', blog_views.dar_like, name='dar_like'),
    path('dar-dislike/<int:pk>/', blog_views.dar_dislike, name='dar_dislike'),
    
    # Home principal
    path('', usuarios_views.home, name='home'),

    # Página "Quiénes somos"
    path('quienes-somos/', usuarios_views.quienes_somos, name='quienes_somos'),

    # Página "Profesionales de la salud"
    path('profesionales/', usuarios_views.profesionales, name='profesionales'),

    # Registro de usuarios
    path('registro/', usuarios_views.registro, name='registro'),

    # Login usando la vista de Django
    path('login/', auth_views.LoginView.as_view(), name='login'),

    # Logout personalizado que redirige al home
    path('logout/', usuarios_views.custom_logout, name='logout'),

    # Vista de perfil corregida (coincide con el HTML)
    path('mi-perfil/', usuarios_views.mi_perfil, name='perfil'),

    # Panel exclusivo para médicos
    path('panel-medico/', usuarios_views.panel_medico, name='panel_medico'),

    # Admin
    path('admin/', admin.site.urls),
]