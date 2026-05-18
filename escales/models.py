from django.db import models
from django.utils.text import slugify


class Pais(models.Model):
    nom_pais = models.CharField(max_length=20, primary_key=True)
    slug = models.SlugField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nom_pais}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_pais}"

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Països"


class Escala(models.Model):
    nom_pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    id_escala = models.CharField(max_length=50)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = slugify(f"{self.nom_pais}-{self.id_escala}")
            slug = base_slug
            counter = 1
            while Escala.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_pais} - {self.id_escala}"

    class Meta:
        unique_together = ("nom_pais", "id_escala")
        verbose_name = "Escala"
        verbose_name_plural = "Escales"


class ValorEscala(models.Model):
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE)
    valor_origen = models.CharField(max_length=10)
    valor_upc = models.DecimalField(max_digits=6, decimal_places=2)
    matricula = models.BooleanField()

    def __str__(self):
        return f"{self.escala.nom_pais} - {self.escala.id_escala} - {self.valor_origen}"

    class Meta:
        unique_together = ("escala", "valor_origen")
        verbose_name = "Valor escala"
        verbose_name_plural = "Valors escales"


class Pagina(models.Model):
    num_pagina = models.IntegerField(primary_key=True)
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.num_pagina} - {self.escala.nom_pais} - {self.escala.id_escala}"

    class Meta:
        verbose_name = "Pàgina"
        verbose_name_plural = "Pàgines"


class Universitat(models.Model):
    codi_universitat = models.CharField(max_length=20, primary_key=True)
    nom_universitat = models.CharField(max_length=100)
    facultat = models.CharField(max_length=100, blank=True)
    programa = models.CharField(max_length=40, null=True, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, null=True, blank=True)
    escala = models.ManyToManyField(Escala, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.codi_universitat}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codi_universitat}"
