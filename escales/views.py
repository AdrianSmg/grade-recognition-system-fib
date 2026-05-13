from django.shortcuts import render, get_object_or_404
from .models import Escala, ValorEscala, Universitat
from collections import defaultdict


# Create your views here.
def escales(request):
    escales = Escala.objects.all().order_by("nom_pais", "id_escala")
    escales_by_country = defaultdict(list)
    for escala in escales:
        escales_by_country[escala.nom_pais].append(escala)
    context = {
        "escales_by_country": dict(escales_by_country),
        "total_escales": escales.count(),
    }
    return render(request, "escales/escales.html", context)


def id(request, slug):
    escala_act = get_object_or_404(Escala, slug=slug)
    valors_escala_act = ValorEscala.objects.filter(
        escala=escala_act,
    )
    universitats = Universitat.objects.filter(
        escala=escala_act,
    )
    context = {
        "escala_act": escala_act,
        "valors_escala_act": valors_escala_act,
        "universitats": universitats,
    }
    return render(request, "escales/id.html", context)
