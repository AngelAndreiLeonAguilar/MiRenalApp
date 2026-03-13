from django.contrib import admin
from .models import Opinion

@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'estrellas', 'fecha_creacion')
    list_filter = ('estrellas', 'fecha_creacion')
    search_fields = ('comentario', 'usuario__username')