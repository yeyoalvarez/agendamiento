from django.shortcuts import render
from apps.profesionales.models import profesional
from django_filters.views import FilterView

# crear clases para ver los medicos

class ListaMedicos(FilterView):
    model = Profesional
    # en que template aparecera
    template_name = "buscador/buscador_profesional.html"
    # limita la cantidad de objetos en pantalla y muestra paginado
    paginate_by = 3
