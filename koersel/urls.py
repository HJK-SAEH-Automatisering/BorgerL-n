from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("koersel/<int:pk>/upload/", views.upload, name="upload"),
    path("koersel/<int:pk>/gennemse/", views.gennemse, name="gennemse"),
    path("koersel/<int:pk>/undtagelser/", views.undtagelser, name="undtagelser"),
    path("koersel/<int:pk>/godkend/", views.godkend, name="godkend"),
    path("koersel/<int:pk>/grundlag/<int:resultat>/", views.grundlag, name="grundlag"),
    path("koersel/<int:pk>/eksport/", views.eksport, name="eksport"),
    path("rapport/<int:pk>/", views.rapport, name="rapport"),
]
