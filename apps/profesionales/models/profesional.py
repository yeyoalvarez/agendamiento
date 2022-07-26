from django.contrib.postgres import fields as postgres_fields
from django.db import models

from apps.base.models import TimestampedModel

class especialidad(models.Model):
    nombre_especialidad = models.CharField('Especialidad',max_length=25, blank=False, null=False)

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['nombre_especialidad']

    def __str__(self):
        return self.nombre_especialidad


class Profesional(TimestampedModel):
    GRADOS_ESTUDIO=(
        ('Doctor','Dr'),
        ('Licenciado','Lic')
    )
    mostrar = models.BooleanField(default=True)
    grado = models.CharField(choices = GRADOS_ESTUDIO,max_length=50,
                             help_text="Grado academico alcanzado por el profesional")
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    especialidades = models.ManyToManyField("especialidad",help_text="Especialidades del medico")

    @property
    def img(self):
        from random import choice

        pictures = [
            "img/default_profile/pic0.jpg",
            "img/default_profile/pic1.jpg",
            "img/default_profile/pic2.jpg",
            "img/default_profile/pic3.jpg",
            "img/default_profile/pic4.jpg",
            "img/default_profile/pic5.jpg",
            "img/default_profile/pic6.jpg",
            "img/default_profile/pic7.jpg",
            "img/default_profile/pic8.jpg",
            "img/default_profile/pic9.jpg",
        ]
        return choice(pictures)

    def __str__(self):
        return f"{self.grado} {self.apellidos}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        esp = []
        for especialidad in self.especialidades:
            esp.append(especialidad.lower())
        self.especialidades = esp
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name_plural = "Profesionales"

    def get_full_name(self):
        return f"{self.grado} {self.nombres} {self.apellidos}"

    def get_short_name(self):
        return f"{self.grado} {self.apellidos}"

    def get_horarios_agrupados(self):
        horarios = {}
        for horario in self.horarios.all():
            esp_list = horario.especialidades if horario.especialidades else horario.profesional.especialidades
            especialidades = str(", ".join(esp_list))
            if especialidades not in horarios:
                horarios[especialidades] = {"especialidades": especialidades, "horarios": []}
            horarios[especialidades]["horarios"].append(
                {
                    "horario_id": horario.pk,
                    "dia": horario.dia,
                    "dia_display": horario.get_dia_display(),
                    "horario": horario.get_range(),
                    "mpp": horario.mpp,
                }
            )
        return horarios.values()
