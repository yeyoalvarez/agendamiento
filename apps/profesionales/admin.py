from django.contrib import admin
from .models import HorarioProfesional, Profesional
from .models.profesional import especialidad


class HorarioProfesionalInline(admin.TabularInline):
    extra = 1
    model = HorarioProfesional


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ["get_full_name"]
    inlines = [HorarioProfesionalInline]

@admin.register(especialidad)
class especialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre_especialidad']
