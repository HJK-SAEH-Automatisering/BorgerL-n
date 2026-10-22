from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    tidspunkt = models.DateTimeField(auto_now_add=True, db_index=True)
    bruger = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    handling = models.CharField(max_length=80)
    objekt_type = models.CharField(max_length=60, blank=True)
    objekt_id = models.CharField(max_length=40, blank=True)
    detaljer = models.TextField(blank=True)

    class Meta:
        ordering = ["-tidspunkt", "-id"]
        verbose_name = "auditlog"
        verbose_name_plural = "auditlog"

    def __str__(self):
        return f"{self.tidspunkt:%Y-%m-%d %H:%M} {self.handling}"


def log(bruger, handling: str, objekt=None, detaljer: str = "") -> AuditLog:
    return AuditLog.objects.create(
        bruger=bruger if getattr(bruger, "is_authenticated", False) else None,
        handling=handling,
        objekt_type=objekt.__class__.__name__ if objekt is not None else "",
        objekt_id=str(objekt.pk) if objekt is not None else "",
        detaljer=detaljer,
    )
