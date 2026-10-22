from datetime import date
from decimal import Decimal

from django.db import models


class ZonePris(models.Model):
    antal_zoner = models.PositiveSmallIntegerField()
    gyldig_fra = models.DateField(help_text="Takster fra Nordjyllands Trafikselskab ændres typisk 1. januar.")
    kontant_voksen = models.DecimalField(max_digits=8, decimal_places=2)
    kontant_barn = models.DecimalField("Kontantbillet barn/67", max_digits=8, decimal_places=2)
    pendler_voksen = models.DecimalField(max_digits=8, decimal_places=2)
    pendler_barn = models.DecimalField("Pendlerkort barn/67", max_digits=8, decimal_places=2)
    rejsekort = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["-gyldig_fra", "antal_zoner"]
        constraints = [models.UniqueConstraint(fields=["antal_zoner", "gyldig_fra"], name="unik_zonepris_pr_dato")]
        verbose_name = "zonepris"
        verbose_name_plural = "zonepriser"

    def __str__(self):
        return f"{self.antal_zoner} zoner fra {self.gyldig_fra:%d.%m.%Y}"

    @classmethod
    def gaeldende(cls, pr_dato: date | None = None) -> dict[int, "ZonePris"]:
        pr_dato = pr_dato or date.today()
        resultat: dict[int, ZonePris] = {}
        for pris in cls.objects.filter(gyldig_fra__lte=pr_dato).order_by("antal_zoner", "-gyldig_fra"):
            resultat.setdefault(pris.antal_zoner, pris)
        return resultat


class Parameter(models.Model):
    MAX_EGENBETALING = "max_egenbetaling_procent"
    AFSTANDSKRAV = "afstandskrav_km"

    noegle = models.CharField(max_length=60)
    vaerdi = models.DecimalField(max_digits=8, decimal_places=2)
    gyldig_fra = models.DateField(default=date(2000, 1, 1))
    beskrivelse = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ["noegle", "-gyldig_fra"]
        constraints = [models.UniqueConstraint(fields=["noegle", "gyldig_fra"], name="unik_parameter_pr_dato")]
        verbose_name = "parameter"
        verbose_name_plural = "parametre"

    def __str__(self):
        return f"{self.noegle} = {self.vaerdi}"

    @classmethod
    def hent(cls, noegle: str, pr_dato: date | None = None) -> Decimal:
        pr_dato = pr_dato or date.today()
        raekke = cls.objects.filter(noegle=noegle, gyldig_fra__lte=pr_dato).order_by("-gyldig_fra").first()
        if raekke is None:
            raise LookupError(f"Parameteren '{noegle}' er ikke oprettet i stamdata.")
        return raekke.vaerdi
