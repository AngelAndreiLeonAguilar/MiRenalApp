from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import RegistroForm
from .models import Perfil  # 🔹 Importamos el modelo Perfil
from .decorators import medico_required  # 🔹 Importamos el decorador que creamos
from django.contrib.auth.decorators import login_required  # 🔹 Para proteger vistas de usuarios logueados

# Página principal
def home(request):
    return render(request, "home.html")

# Registro de usuarios
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()  # guarda el nuevo usuario
            # 🔹 Crear perfil automáticamente como paciente
            Perfil.objects.create(user=usuario, tipo="paciente")
            return redirect("login")  # redirige al login después de registrarse
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})

# Logout personalizado
def custom_logout(request):
    logout(request)  # Cierra la sesión
    return redirect("home")  # Redirige al home como invitado

# Panel exclusivo para médicos
@medico_required
def panel_medico(request):
    return render(request, "usuarios/panel_medico.html")

# Vista de perfil del usuario autenticado
@login_required
def mi_perfil(request):
    perfil = Perfil.objects.get(user=request.user)
    return render(request, "usuarios/mi_perfil.html", {"perfil": perfil})

# Página "Quiénes somos"
def quienes_somos(request):
    return render(request, "quienes_somos.html")

# Página "Profesionales de la salud"
def profesionales(request):
    return render(request, "profesionales.html")