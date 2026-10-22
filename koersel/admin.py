from django.contrib import admin

from .models import Beregningskoersel, Koersel


class SkrivebeskyttetAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Koersel)
class KoerselAdmin(SkrivebeskyttetAdmin):
    list_display = ("maaned", "status", "filnavn", "oprettet_af", "oprettet")


@admin.register(Beregningskoersel)
class BeregningskoerselAdmin(SkrivebeskyttetAdmin):
    list_display = ("rapport_id", "koersel", "tidspunkt", "bruger", "pdf_sha256")
    exclude = ("snapshot",)
