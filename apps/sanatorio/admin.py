from django.contrib import admin
from .models import HorarioProfesional, Profesional

class HorarioProfesionalInline(admin.TabularInline):
    extra = 1
    model = HorarioProfesional


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ["id", "get_full_name"]
    inlines = [HorarioProfesionalInline]
