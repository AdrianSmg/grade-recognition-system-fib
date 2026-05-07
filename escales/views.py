from django.shortcuts import render, get_object_or_404
from .models import Escala, ValorEscala


# Create your views here.
def main(request):
    return render(request, "main.html")


def id(request, pais, id_esc):
    escala_act = get_object_or_404(Escala, nom_pais=pais, id_escala=id_esc)
    valors_escala_act = ValorEscala.objects.filter(
        escala__nom_pais=pais, escala__id_escala=id_esc
    )
    context = {
        "escala_act": escala_act,
        "valors_escala_act": valors_escala_act,
    }
    return render(request, "escales/id.html", context)
