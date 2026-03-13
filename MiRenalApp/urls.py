from django.contrib import admin
from django.urls import path
from apps.usuarios import views as usuarios_views
from django.contrib.auth import views as auth_views
from apps.blog import views as blog_views 

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Rutas del Foro
    path('foro/', blog_views.foro, name='foro'),
    path('dar-like/<int:pk>/', blog_views.dar_like, name='dar_like'),
    path('dar-dislike/<int:pk>/', blog_views.dar_dislike, name='dar_dislike'),
    
    # Moderación (ADMIN) - Corregido con blog_views
    path('eliminar/<int:opinion_id>/', blog_views.eliminar_comentario, name='eliminar_comentario'),
    path('bloquear/<int:usuario_id>/', blog_views.alternar_bloqueo, name='alternar_bloqueo'),

    # Home y Páginas Informativas
    path('', usuarios_views.home, name='home'),
    path('quienes-somos/', usuarios_views.quienes_somos, name='quienes_somos'),
    path('profesionales/', usuarios_views.profesionales, name='profesionales'),

    # Autenticación y Perfil
    path('registro/', usuarios_views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', usuarios_views.custom_logout, name='logout'),
    path('mi-perfil/', usuarios_views.mi_perfil, name='perfil'),
    path('panel-medico/', usuarios_views.panel_medico, name='panel_medico'),
    
    #RECUPERACIÓN DE CONTRASEÑA

    # 1. El usuario ingresa su email
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='usuarios/password_reset.html'), 
         name='password_reset'),

    # 2. Mensaje de "Correo enviado"
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), 
         name='password_reset_done'),

    # 3. El link que llega al correo (maneja el token de seguridad)
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    # 4. Mensaje de "Contraseña cambiada con éxito"
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), 
         name='password_reset_complete'),
]