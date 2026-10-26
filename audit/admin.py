from django.contrib import admin

from .models import AuditLog

# Klassenavnet gemmes som data og ændres ikke; det er kun visningen, der bruger det nye ord.
VISNINGSNAVN = {"Borger": "Medarbejder"}


def objekt_type_navn(objekt_type: str) -> str:
    return VISNINGSNAVN.get(objekt_type, objekt_type)


class ObjektTypeFilter(admin.SimpleListFilter):
    title = "objekt type"
    parameter_name = "objekt_type"

    def lookups(self, request, model_admin):
        typer = model_admin.get_queryset(request).exclude(objekt_type="").order_by("objekt_type").values_list("objekt_type", flat=True).distinct()
        return [(t, objekt_type_navn(t)) for t in typer]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(objekt_type=self.value())
        return queryset


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("tidspunkt", "bruger", "handling", "objekt_type_visning", "objekt_id")
    list_filter = ("handling", ObjektTypeFilter)
    search_fields = ("detaljer", "handling")

    @admin.display(description="objekt type", ordering="objekt_type")
    def objekt_type_visning(self, obj):
        return objekt_type_navn(obj.objekt_type)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
