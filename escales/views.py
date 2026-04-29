from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Escala


# Create your views here.
def main(request):
    pass


def id(request):
    id_act = Escala.objects.get(id=id)
    template = loader.get_template("id.html")
    context = {
        "id_act": id_act,
    }
    return HttpResponse(template.render(context, request))
