from django.contrib import admin

from audit.models import log

from .models import Afdeling, Borger


@admin.register(Afdeling)
class AfdelingAdmin(admin.ModelAdmin):
    list_display = ("navn", "lonseddel_modtager")


@admin.register(Borger)
class BorgerAdmin(admin.ModelAdmin):
    list_display = ("navn", "tj_nr", "afdeling", "afstand_km", "transport", "aktiv")
    list_filter = ("afdeling", "aktiv", "transport")
    search_fields = ("navn", "tj_nr")
    exclude = ("cpr",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        log(request.user, "Ændrede borger i admin" if change else "Oprettede borger i admin", obj, obj.navn)
