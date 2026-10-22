from django.contrib import admin

from audit.models import log

from .models import Parameter, ZonePris


class AuditeretAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        log(request.user, "Ændrede stamdata" if change else "Oprettede stamdata", obj, str(obj))

    def delete_model(self, request, obj):
        log(request.user, "Slettede stamdata", obj, str(obj))
        super().delete_model(request, obj)


@admin.register(ZonePris)
class ZonePrisAdmin(AuditeretAdmin):
    list_display = ("antal_zoner", "gyldig_fra", "kontant_barn", "pendler_barn", "kontant_voksen", "pendler_voksen")
    list_filter = ("gyldig_fra",)


@admin.register(Parameter)
class ParameterAdmin(AuditeretAdmin):
    list_display = ("noegle", "vaerdi", "gyldig_fra", "beskrivelse")
