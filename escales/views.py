from django.shortcuts import render, get_object_or_404
from .models import Escala


# Create your views here.
def main(request):
    return render(request, "main.html")


def id(request, id_escala):
    id_act = get_object_or_404(Escala, id=id_escala)
    context = {
        "id_act": id_act,
    }
    return render(request, "escales/id.html", context)
