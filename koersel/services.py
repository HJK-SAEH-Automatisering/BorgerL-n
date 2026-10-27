import csv
import hashlib
import io
import json
from collections import Counter
from decimal import Decimal

from django.core.files.base import ContentFile
from django.db import transaction
from django.utils import timezone

from audit.models import log
from beregning import engine
from beregning.pdf import LAYOUT_VERSION, lav_rapport
from register.models import Borger, normaliser_navn
from stamdata.models import Parameter, ZonePris

from .importer import Raekke
from .models import Beregningskoersel, Koersel, Linje, LinjeResultat, maanedsnavn


class BeregningsFejl(Exception):
    def __init__(self, fejl_pr_linje: dict[int, list[str]], generelt: list[str] | None = None):
        self.fejl_pr_linje = fejl_pr_linje
        self.generelt = generelt or []
        super().__init__("Beregningen kan ikke køres.")


def opret_linjer(koersel: Koersel, raekker: list[Raekke], filnavn: str, bruger=None) -> None:
    antal_pr_navn = Counter(normaliser_navn(r.navn) for r in raekker)
    borgere_pr_navn: dict[str, list[Borger]] = {}
    for b in Borger.objects.filter(aktiv=True):
        borgere_pr_navn.setdefault(normaliser_navn(b.navn), []).append(b)
    with transaction.atomic():
        koersel.linjer.all().delete()
        for r in raekker:
            nøgle = normaliser_navn(r.navn)
            linje = Linje(
                koersel=koersel,
                raekke=r.raekke,
                fil_navn=r.navn,
                minutter=r.minutter,
                fil_dage=r.dage,
                dobbelt=antal_pr_navn[nøgle] > 1,
            )
            kandidater = borgere_pr_navn.get(nøgle, [])
            if len(kandidater) == 1:
                linje.saet_borger(kandidater[0])
            elif len(kandidater) > 1:
                linje.match_status = Linje.Match.FLERTYDIG
                linje.kandidater = ",".join(str(b.pk) for b in kandidater)
            linje.save()
        koersel.filnavn = filnavn
        koersel.uploadet_af = bruger
        koersel.uploadet = timezone.now()
        koersel.status = Koersel.Status.KLADDE
        koersel.save()


def uafklarede(koersel: Koersel):
    return koersel.linjer.exclude(match_status=Linje.Match.MATCHET)


def tilgaengelige_zoner(pr_dato) -> list[int]:
    return sorted(ZonePris.gaeldende(pr_dato))


def linje_fejl(linje: Linje, par, zonepriser) -> list[str]:
    if linje.borger_id is None:
        return ["Medarbejderen er ikke afklaret."]
    return engine.valider(byg_input(linje, dobbelt=False), zonepriser)


def byg_input(linje: Linje, dobbelt: bool) -> engine.Input:
    b = linje.borger
    return engine.Input(
        navn=b.navn if b else linje.fil_navn,
        tj_nr=b.tj_nr if b else None,
        minutter=linje.minutter,
        sats=b.sats if b else None,
        traek_procent=b.traek_procent if b else Decimal("40"),
        transport=linje.transport,
        zoner=linje.zoner,
        individuel=linje.individuel,
        dage=linje.dage,
        afstand_km=b.afstand_km if b else Decimal("0"),
        dobbelt=dobbelt,
    )


def hent_parametre(pr_dato) -> tuple[engine.Parametre, dict[int, engine.Zonepris], dict[int, ZonePris]]:
    priser = ZonePris.gaeldende(pr_dato)
    grundzoner = 2
    if grundzoner not in priser:
        raise BeregningsFejl({}, [f"Zonetabellen mangler prisen for {grundzoner} zoner (grundtakst)."])
    par = engine.Parametre(
        max_egenbetaling_procent=Parameter.hent(Parameter.MAX_EGENBETALING, pr_dato),
        afstandskrav_km=Parameter.hent(Parameter.AFSTANDSKRAV, pr_dato),
        grundtakst=priser[grundzoner].pendler_barn,
        grundtakst_zoner=grundzoner,
    )
    zoner = {z: engine.Zonepris(kontant_barn=p.kontant_barn, pendler_barn=p.pendler_barn) for z, p in priser.items()}
    return par, zoner, priser


def _kilder(linje: Linje) -> dict[str, str]:
    b = linje.borger

    def kilde(værdi, register_værdi):
        return "register" if værdi == register_værdi else "manuelt"

    return {
        "timer": "fil",
        "sats": "register",
        "traek_procent": "register",
        "afstand_km": "register",
        "transport": kilde(linje.transport, b.transport),
        "zoner": kilde(linje.zoner, b.zoner),
        "individuel": "manuelt" if linje.individuel else "-",
        "dage": "manuelt" if linje.individuel else "-",
    }


def valider_koersel(koersel: Koersel) -> dict[int, list[str]]:
    par, zoner, _ = hent_parametre(koersel.maaned)
    fejl = {}
    for linje in koersel.linjer.select_related("borger"):
        f = linje_fejl(linje, par, zoner)
        if f:
            fejl[linje.pk] = f
    return fejl


@transaction.atomic
def koer_beregning(koersel: Koersel, bruger) -> Beregningskoersel:
    linjer = list(koersel.linjer.select_related("borger", "borger__afdeling"))
    if not linjer:
        raise BeregningsFejl({}, ["Der er ingen medarbejdere at beregne. Upload en timefil først."])
    par, zoner, priser = hent_parametre(koersel.maaned)
    antal_pr_borger = Counter(l.borger_id for l in linjer if l.borger_id)

    fejl: dict[int, list[str]] = {}
    resultater = []
    for linje in linjer:
        if linje.borger_id is None:
            fejl[linje.pk] = ["Medarbejderen er ikke afklaret."]
            continue
        dobbelt = linje.dobbelt or antal_pr_borger[linje.borger_id] > 1
        res = engine.beregn(byg_input(linje, dobbelt), par, zoner)
        if res.fejl:
            fejl[linje.pk] = res.fejl
        resultater.append((linje, res))
    if fejl:
        raise BeregningsFejl(fejl)

    nummer = (koersel.beregninger.order_by("-nummer").values_list("nummer", flat=True).first() or 0) + 1
    nu = timezone.localtime()
    totaler = {
        "antal": len(resultater),
        "loen_foer": str(sum((r.loen_foer for _, r in resultater), Decimal("0"))),
        "loen_efter": str(sum((r.loen_efter for _, r in resultater), Decimal("0"))),
        "traek_991": str(sum((r.traek_991 for _, r in resultater), Decimal("0"))),
        "udbetaling_991": str(sum((r.udbetaling_991 for _, r in resultater), Decimal("0"))),
    }
    brugte_zoner = {2} | {l.zoner for l, _ in resultater if l.zoner is not None}
    snapshot = {
        "version": 1,
        "rapport_layout": LAYOUT_VERSION,
        "rapport_id": f"{koersel.maaned:%Y-%m}-{nummer:03d}",
        "maaned": f"{koersel.maaned:%Y-%m}",
        "maaned_tekst": maanedsnavn(koersel.maaned),
        "tidspunkt_tekst": nu.strftime("%d.%m.%Y kl. %H:%M"),
        "bruger": (bruger.get_full_name() or bruger.get_username()) if bruger else "-",
        "filnavn": koersel.filnavn,
        "parametre": {
            "max_egenbetaling_procent": str(par.max_egenbetaling_procent),
            "afstandskrav_km": str(par.afstandskrav_km),
            "grundtakst": str(par.grundtakst),
            "grundtakst_zoner": par.grundtakst_zoner,
            "zonepriser_gyldig_fra": f"{max(p.gyldig_fra for z, p in priser.items() if z in brugte_zoner):%d.%m.%Y}",
        },
        "zonepriser": {
            str(z): {"kontant_barn": str(priser[z].kontant_barn), "pendler_barn": str(priser[z].pendler_barn)}
            for z in sorted(brugte_zoner)
            if z in priser
        },
        "totaler": totaler,
        "linjer": [],
    }
    for linje, res in resultater:
        b = linje.borger
        snapshot["linjer"].append(
            {
                "linje_id": linje.pk,
                "navn": b.navn,
                "tj_nr": b.tj_nr or "",
                "afdeling": b.afdeling.navn if b.afdeling else "",
                "input": {
                    "minutter": linje.minutter,
                    "sats": str(b.sats),
                    "traek_procent": str(b.traek_procent),
                    "afstand_km": str(b.afstand_km),
                    "transport": linje.transport,
                    "zoner": linje.zoner,
                    "individuel": linje.individuel,
                    "dage": linje.dage,
                },
                "kilder": _kilder(linje),
                "advarsler": res.advarsler,
                "resultat": res.til_dict(),
                "grundlag": res.grundlag,
            }
        )

    pdf_bytes = lav_rapport(snapshot)
    beregning = Beregningskoersel(
        koersel=koersel,
        nummer=nummer,
        bruger=bruger,
        snapshot=json.dumps(snapshot, ensure_ascii=False),
        pdf_sha256=hashlib.sha256(pdf_bytes).hexdigest(),
    )
    beregning.pdf.save(f"beregning-{snapshot['rapport_id']}.pdf", ContentFile(pdf_bytes), save=False)
    beregning.save()
    for i, (linje, res) in enumerate(resultater):
        b = linje.borger
        LinjeResultat.objects.create(
            beregning=beregning,
            indeks=i,
            linje=linje,
            navn=b.navn,
            tj_nr=b.tj_nr or "",
            afdeling=b.afdeling.navn if b.afdeling else "",
            timer_minutter=linje.minutter,
            loen_foer=res.loen_foer,
            loen_efter=res.loen_efter,
            traek_991=res.traek_991,
            udbetaling_991=res.udbetaling_991,
        )
    koersel.status = Koersel.Status.BEREGNET
    koersel.save(update_fields=["status"])
    log(bruger, "Kørte beregning", beregning, f"{koersel.navn}, rapport {beregning.rapport_id}, {len(resultater)} medarbejdere")
    return beregning


@transaction.atomic
def godkend(beregning: Beregningskoersel, bruger, resultat_id: int | None = None) -> int:
    if not beregning.er_aktiv:
        raise ValueError("Kun den nyeste beregning kan godkendes.")
    qs = beregning.resultater.filter(godkendt=False)
    if resultat_id is not None:
        qs = qs.filter(pk=resultat_id)
    antal = qs.update(godkendt=True, godkendt_af=bruger, godkendt_tidspunkt=timezone.now())
    if antal:
        log(bruger, "Godkendte beregning", beregning, f"{antal} linjer, rapport {beregning.rapport_id}")
    if beregning.alle_godkendt:
        Koersel.objects.filter(pk=beregning.koersel_id).update(status=Koersel.Status.GODKENDT)
    return antal


@transaction.atomic
def genaabn(beregning: Beregningskoersel, bruger) -> tuple[int, bool]:
    """Fjerner alle godkendelser på beregningen og sætter en godkendt kørsel tilbage til beregnet.

    Returnerer antal fjernede godkendelser og om kørslen var godkendt. Har det ingen virkning,
    ændres og logges intet."""
    koersel = beregning.koersel
    var_godkendt = koersel.status == Koersel.Status.GODKENDT
    antal = beregning.resultater.filter(godkendt=True).update(godkendt=False, godkendt_af=None, godkendt_tidspunkt=None)
    if var_godkendt:
        koersel.status = Koersel.Status.BEREGNET
        koersel.save(update_fields=["status"])
    if var_godkendt or antal:
        log(bruger, "Genåbnede kørsel", koersel, f"{koersel.navn}, fjernede godkendelser: {antal}")
    return antal, var_godkendt


def kan_eksportere(koersel: Koersel) -> bool:
    b = koersel.aktiv_beregning
    return bool(b and b.alle_godkendt and koersel.status == Koersel.Status.GODKENDT)


def _dk(v: Decimal) -> str:
    return f"{v:.2f}".replace(".", ",")


def lav_csv(beregning: Beregningskoersel) -> bytes:
    ud = io.StringIO()
    w = csv.writer(ud, delimiter=";")
    w.writerow(["Tj.nr.", "Navn", "Afdeling", "Timer (lønart 110)", "Løn før skat", "Træk lønart 991", "Udbetaling lønart 991"])
    for r in beregning.resultater.all():
        w.writerow(
            [
                r.tj_nr,
                r.navn,
                r.afdeling,
                _dk(Decimal(r.timer_minutter) / 60),
                _dk(r.loen_foer),
                _dk(r.traek_991),
                _dk(r.udbetaling_991),
            ]
        )
    return ud.getvalue().encode("utf-8-sig")
