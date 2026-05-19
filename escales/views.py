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


def universitats(request):
    universitats = Universitat.objects.all().order_by(
        "pais__nom_pais", "nom_universitat"
    )
    universitats_by_country = defaultdict(list)
    for universitat in universitats:
        if universitat.pais:
            universitats_by_country[universitat.pais].append(universitat)
        else:
            universitats_by_country["Sense país assignat"].append(universitat)
    context = {
        "universitats_by_country": dict(universitats_by_country),
        "total_universitats": universitats.count(),
    }
    return render(request, "escales/universitats.html", context)


def id_universitat(request, slug):
    universitat = get_object_or_404(Universitat, slug=slug)
    escales = universitat.escala.all()
    escales_amb_valors = []
    for escala in escales:
        valors = ValorEscala.objects.filter(escala=escala)
        escales_amb_valors.append(
            {
                "escala": escala,
                "valors": valors,
            }
        )
    context = {
        "universitat": universitat,
        "escales_amb_valors": escales_amb_valors,
    }
    return render(request, "escales/id_universitat.html", context)
