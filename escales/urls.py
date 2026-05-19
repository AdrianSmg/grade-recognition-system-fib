from django.urls import path
from . import views

urlpatterns = [
    path("", views.escales, name="escales"),
    path("universitats/", views.universitats, name="universitats"),
    path("universitats/<slug:slug>/", views.id_universitat, name="id_universitat"),
    path("<slug:slug>/", views.id, name="id"),
]
