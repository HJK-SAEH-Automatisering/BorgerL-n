from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("tidspunkt", "bruger", "handling", "objekt_type", "objekt_id")
    list_filter = ("handling", "objekt_type")
    search_fields = ("detaljer", "handling")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
