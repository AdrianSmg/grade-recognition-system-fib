from django.urls import path
from . import views

urlpatterns = [
    path("", views.escales, name="escales"),
    path("<slug:slug>/", views.id, name="id"),
]
