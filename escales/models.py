from django.db import models


class Escala(models.Model):
    nom_pais = models.CharField(max_length=30)
    id_escala = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nom_pais} - {self.id_escala}"

    class Meta:
        unique_together = ("nom_pais", "id_escala")


class ValorEscala(models.Model):
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE)
    valor_origen = models.CharField(max_length=10)
    valor_upc = models.DecimalField(max_digits=4, decimal_places=2)
    matricula = models.BooleanField()

    def __str__(self):
        return f"{self.escala.nom_pais} - {self.escala.id_escala} - {self.valor_origen}"

    class Meta:
        unique_together = ("escala", "valor_origen")


class Pagina(models.Model):
    num_pagina = models.IntegerField(primary_key=True)
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.num_pagina} - {self.escala.nom_pais} - {self.escala.id_escala}"
