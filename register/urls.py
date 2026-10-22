from django.urls import path

from . import views

urlpatterns = [
    path("", views.borger_liste, name="borger_liste"),
    path("ny/", views.borger_ny, name="borger_ny"),
    path("<int:pk>/", views.borger_ret, name="borger_ret"),
    path("<int:pk>/cpr/", views.vis_cpr, name="vis_cpr"),
]
