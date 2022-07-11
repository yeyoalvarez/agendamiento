from django.contrib.postgres import fields as postgres_fields
from django.db import models

from apps.base.models import TimestampedModel, UuidAsPkModel

LUNES = 1
MARTES = 2
MIERCOLES = 3
JUEVES = 4
VIERNES = 5
SABADO = 6
DOMINGO = 7
DIAS = (
    (LUNES, "Lunes"),
    (MARTES, "Martes"),
    (MIERCOLES, "Miercoles"),
    (JUEVES, "Jueves"),
    (VIERNES, "Viernes"),
    (SABADO, "Sábado"),
    (DOMINGO, "Domingo"),
)


class HorarioProfesional(TimestampedModel, UuidAsPkModel):
    profesional = models.ForeignKey("sanatorio.Profesional", on_delete=models.CASCADE, related_name="horarios")
    dia = models.PositiveSmallIntegerField(default=DOMINGO, choices=DIAS)
    hora_inicio = models.PositiveSmallIntegerField(choices=((x, x) for x in range(0, 24)), default=12)
    minuto_inicio = models.PositiveSmallIntegerField(choices=((x, x) for x in range(0, 46, 15)), default=0)
    hora_fin = models.PositiveSmallIntegerField(
        choices=((x, x) for x in range(0, 24)), blank=True, null=True, help_text="en blanco para no mostrar"
    )
    minuto_fin = models.PositiveSmallIntegerField(
        choices=((x, x) for x in range(0, 46, 15)), blank=True, null=True, help_text="en blanco para no mostrar"
    )
    mpp = models.PositiveSmallIntegerField("Minutos por paciente", default=0, help_text="0 para no mostrar")
    especialidades = postgres_fields.ArrayField(
        models.CharField(max_length=255), help_text="Especialidades que atiende en este horario", blank=True
    )

    def __str__(self):
        return f"{self.dia} {self.hora_inicio} Profesional{self.profesional.id}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.hora_fin and not self.minuto_fin:
            self.minuto_fin = 0
        elif self.minuto_fin and not self.hora_fin:
            self.minuto_fin = None
        super().save(force_insert, force_update, using, update_fields)

    def get_inicio(self):
        return f"{f'{str(self.hora_inicio).zfill(2)}:{str(self.minuto_inicio).zfill(2)}'}"

    def get_fin(self):
        if self.hora_fin:
            return f"{f'{str(self.hora_fin).zfill(2)}:{str(self.minuto_fin).zfill(2)}'}"
        else:
            return None

    def get_range(self):
        if fin := self.get_fin():
            return f"de {self.get_inicio()}Hs. a {fin}Hs."
        return f"a partir de las {self.get_inicio()}Hs."
