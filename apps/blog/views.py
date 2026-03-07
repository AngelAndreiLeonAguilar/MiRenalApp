# apps/blog/views.py
from django.shortcuts import render

def foro(request):
    # Por ahora enviamos una lista vacía para que cargue el HTML
    return render(request, 'blog/foro.html', {'opiniones': []})

def dar_like(request, pk):
    pass # Implementaremos la lógica después

def dar_dislike(request, pk):
    pass