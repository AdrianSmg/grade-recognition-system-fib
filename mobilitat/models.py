from django.db import models
from django.utils.text import slugify
from escales.models import Universitat


class CursAcademic(models.Model):
    curs = models.CharField(max_length=10, primary_key=True)

    class Meta:
        verbose_name = "Curs acadèmic"
        verbose_name_plural = "Cursos acadèmics"


class Durada(models.Model):
    tipus = models.CharField(
        max_length=10,
        primary_key=True,
        choices=[("Q1", "Q1"), ("Q2", "Q2"), ("ANUAL", "Anual")],
    )

    class Meta:
        verbose_name = "Durada"
        verbose_name_plural = "Durades"


class PeriodeMobilitat(models.Model):
    curs = models.ForeignKey(CursAcademic, on_delete=models.PROTECT)
    durada = models.ForeignKey(Durada, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("curs", "durada")
        verbose_name = "Període mobilitat"
        verbose_name_plural = "Períodes mobilitat"


class Estudiant(models.Model):
    codi_exp_mob = models.CharField(max_length=20, primary_key=True)
    nom = models.CharField(max_length=30)
    primer_cognom = models.CharField(max_length=30)
    segon_cognom = models.CharField(max_length=30, blank=True)
    dni = models.CharField(max_length=20, unique=True)
    codi_exp = models.CharField(max_length=20, unique=True)
    centre = models.IntegerField()


class Mobilitat(models.Model):
    periode_mobilitat = models.ForeignKey(PeriodeMobilitat, on_delete=models.PROTECT)
    universitat = models.ForeignKey(Universitat, on_delete=models.PROTECT)
    estudiant = models.ForeignKey(Estudiant, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.estudiant.nom}-{self.periode_mobilitat.curs}-{self.periode_mobilitat.durada}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.estudiant.nom} - {self.universitat.nom_universitat} - {self.periode_mobilitat.curs}-{self.periode_mobilitat.durada}"

    class Meta:
        unique_together = ("periode_mobilitat", "universitat", "estudiant")
