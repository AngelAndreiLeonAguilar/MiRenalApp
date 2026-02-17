from django.shortcuts import redirect
from .models import Perfil

def medico_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                perfil = Perfil.objects.get(user=request.user)
                if perfil.tipo == "medico":
                    return view_func(request, *args, **kwargs)
            except Perfil.DoesNotExist:
                pass
        # Si no es médico, redirige al home
        return redirect("home")
    return wrapper