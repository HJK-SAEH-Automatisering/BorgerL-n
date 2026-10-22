import re
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Transport(models.TextChoices):
    SELV = "selv", "Kører selv"
    TAXA = "taxa", "Taxa"
    INGEN = "ingen", "Ingen udgift"


def normaliser_cpr(vaerdi: str) -> str:
    cifre = re.sub(r"\D", "", vaerdi or "")
    if not cifre:
        return ""
    if len(cifre) != 10:
        raise ValidationError("CPR-nummeret skal have 10 cifre.")
    return f"{cifre[:6]}-{cifre[6:]}"


def normaliser_navn(navn: str) -> str:
    return " ".join((navn or "").split()).casefold()


class Afdeling(models.Model):
    navn = models.CharField(max_length=100, unique=True)
    lonseddel_modtager = models.CharField("Modtager af lønseddel", max_length=100, blank=True)

    class Meta:
        ordering = ["navn"]
        verbose_name_plural = "afdelinger"

    def __str__(self):
        return self.navn


class Borger(models.Model):
    tj_nr = models.CharField("Tj.nr.", max_length=20, unique=True, null=True, blank=True)
    navn = models.CharField(max_length=150, db_index=True)
    cpr = models.CharField("CPR-nummer", max_length=11, blank=True)
    adresse = models.CharField(max_length=250, blank=True)
    afdeling = models.ForeignKey(Afdeling, null=True, blank=True, on_delete=models.SET_NULL)
    arbejdssted = models.CharField(max_length=100, blank=True)
    afstand_km = models.DecimalField("Afstand til arbejdssted (km)", max_digits=5, decimal_places=1, default=Decimal("0.0"))
    transport = models.CharField("Transport", max_length=5, choices=Transport.choices, blank=True)
    zoner = models.PositiveSmallIntegerField("Standard-zoner", null=True, blank=True)
    sats = models.DecimalField("Sats pr. time (kr.)", max_digits=6, decimal_places=2, null=True, blank=True)
    traek_procent = models.DecimalField("Trækprocent", max_digits=4, decimal_places=1, default=Decimal("40.0"))
    aktiv = models.BooleanField(default=True)

    class Meta:
        ordering = ["navn"]
        verbose_name_plural = "borgere"

    def __str__(self):
        return self.navn

    @property
    def cpr_maskeret(self) -> str:
        if not self.cpr:
            return ""
        return "******-" + self.cpr[-4:]

    def save(self, *args, **kwargs):
        self.tj_nr = (self.tj_nr or "").strip() or None
        super().save(*args, **kwargs)
