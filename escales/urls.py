from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("<str:pais>/<str:id_esc>/", views.id, name="id"),
]
