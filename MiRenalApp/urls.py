from django.contrib import admin
from django.urls import path
from apps.usuarios import views as usuarios_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home principal
    path('', usuarios_views.home, name='home'),

    # Registro de usuarios
    path('registro/', usuarios_views.registro, name='registro'),

    # Login usando la vista de Django
    path('login/', auth_views.LoginView.as_view(), name='login'),

    # Logout personalizado que redirige al home
    path('logout/', usuarios_views.custom_logout, name='logout'),

    # Vista de perfil del usuario autenticado
    path('mi-perfil/', usuarios_views.mi_perfil, name='mi_perfil'),

    # Panel exclusivo para médicos
    path('panel-medico/', usuarios_views.panel_medico, name='panel_medico'),

    # Admin
    path('admin/', admin.site.urls),
]