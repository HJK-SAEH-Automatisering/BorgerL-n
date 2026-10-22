import json
from decimal import Decimal

from django.conf import settings
from django.db import models

from register.models import Borger, Transport

MAANEDER = ["januar", "februar", "marts", "april", "maj", "juni", "juli", "august", "september", "oktober", "november", "december"]


def maanedsnavn(dato) -> str:
    return f"{MAANEDER[dato.month - 1]} {dato.year}"


class Koersel(models.Model):
    class Status(models.TextChoices):
        KLADDE = "kladde", "Kladde"
        BEREGNET = "beregnet", "Beregnet"
        GODKENDT = "godkendt", "Godkendt"

    maaned = models.DateField(unique=True, help_text="Første dag i måneden")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.KLADDE)
    filnavn = models.CharField(max_length=255, blank=True)
    oprettet_af = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    oprettet = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-maaned"]
        verbose_name = "kørsel"
        verbose_name_plural = "kørsler"

    def __str__(self):
        return maanedsnavn(self.maaned)

    @property
    def navn(self) -> str:
        return maanedsnavn(self.maaned)

    @property
    def aktiv_beregning(self):
        return self.beregninger.order_by("-nummer").first()


class Linje(models.Model):
    class Match(models.TextChoices):
        MATCHET = "matchet", "Matchet"
        INGEN = "ingen", "Ingen match"
        FLERTYDIG = "flertydig", "Flere mulige"

    koersel = models.ForeignKey(Koersel, on_delete=models.CASCADE, related_name="linjer")
    raekke = models.PositiveIntegerField()
    fil_navn = models.CharField("Navn i filen", max_length=150)
    minutter = models.PositiveIntegerField()
    dobbelt = models.BooleanField(default=False)
    match_status = models.CharField(max_length=10, choices=Match.choices, default=Match.INGEN)
    kandidater = models.CharField(max_length=200, blank=True, help_text="Komma-separerede borger-id'er ved flere mulige")
    borger = models.ForeignKey(Borger, null=True, blank=True, on_delete=models.SET_NULL)
    transport = models.CharField(max_length=5, choices=Transport.choices, blank=True)
    zoner = models.PositiveSmallIntegerField(null=True, blank=True)
    individuel = models.BooleanField(default=False)
    dage = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["raekke"]

    def __str__(self):
        return f"{self.fil_navn} ({self.koersel})"

    @property
    def timer_tekst(self) -> str:
        return f"{self.minutter // 60}:{self.minutter % 60:02d}"

    @property
    def kandidat_ids(self) -> list[int]:
        return [int(x) for x in self.kandidater.split(",") if x]

    def saet_borger(self, borger: Borger) -> None:
        self.borger = borger
        self.match_status = self.Match.MATCHET
        self.kandidater = ""
        self.transport = borger.transport
        self.zoner = borger.zoner
        self.individuel = False
        self.dage = None


class Beregningskoersel(models.Model):
    koersel = models.ForeignKey(Koersel, on_delete=models.PROTECT, related_name="beregninger")
    nummer = models.PositiveIntegerField()
    tidspunkt = models.DateTimeField(auto_now_add=True)
    bruger = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    snapshot = models.TextField(help_text="Uforanderligt JSON-snapshot af inputs, parametre, resultater og beregningsgrundlag")
    pdf = models.FileField(upload_to="rapporter/%Y/%m/")
    pdf_sha256 = models.CharField(max_length=64)

    class Meta:
        ordering = ["-nummer"]
        constraints = [models.UniqueConstraint(fields=["koersel", "nummer"], name="unik_beregning_pr_koersel")]
        verbose_name = "beregningskørsel"
        verbose_name_plural = "beregningskørsler"

    def __str__(self):
        return self.rapport_id

    @property
    def rapport_id(self) -> str:
        return f"{self.koersel.maaned:%Y-%m}-{self.nummer:03d}"

    @property
    def data(self) -> dict:
        return json.loads(self.snapshot)

    @property
    def er_aktiv(self) -> bool:
        return self.nummer == self.koersel.beregninger.aggregate(m=models.Max("nummer"))["m"]

    @property
    def alle_godkendt(self) -> bool:
        return not self.resultater.filter(godkendt=False).exists() and self.resultater.exists()


class LinjeResultat(models.Model):
    beregning = models.ForeignKey(Beregningskoersel, on_delete=models.CASCADE, related_name="resultater")
    indeks = models.PositiveIntegerField(help_text="Placering i snapshottets liste over linjer")
    linje = models.ForeignKey(Linje, null=True, on_delete=models.SET_NULL)
    navn = models.CharField(max_length=150)
    tj_nr = models.CharField(max_length=20, blank=True)
    afdeling = models.CharField(max_length=100, blank=True)
    timer_minutter = models.PositiveIntegerField(default=0)
    loen_foer = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    loen_efter = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    traek_991 = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    udbetaling_991 = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    godkendt = models.BooleanField(default=False)
    godkendt_af = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    godkendt_tidspunkt = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["indeks"]

    @property
    def detaljer(self) -> dict:
        return self.beregning.data["linjer"][self.indeks]
