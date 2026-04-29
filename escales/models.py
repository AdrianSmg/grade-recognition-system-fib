from django.db import models


class Escala(models.Model):
    nom_pais = models.CharField(max_length=30)
    descripcio = models.CharField(max_length=50)
    pagina_document = models.IntegerField()


class ValorEscala(models.Model):
    id_escala = models.ForeignKey(Escala, on_delete=models.CASCADE)
    valor_origen = models.CharField(max_length=10)
    valor_upc = models.DecimalField(max_digits=4, decimal_places=2)
    matricula = models.BooleanField()
