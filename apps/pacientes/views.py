from django.shortcuts import render, redirect
from .forms import PacientesForm
from .models import Pacientes

def dashboard(request):
    # Si el usuario envía el formulario (POST)
    if request.method == "POST":
        form = PacientesForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user  # asigna el usuario logueado
            registro.save()
            return redirect("paciente_dashboard")  # recarga la página para ver el nuevo registro
    else:
        form = PacientesForm()

    # Recuperar los registros del paciente logueado
    registros = Pacientes.objects.filter(usuario=request.user).order_by("-fecha")

    return render(request, "pacientes/dashboard.html", {
        "form": form,
        "registros": registros
    })