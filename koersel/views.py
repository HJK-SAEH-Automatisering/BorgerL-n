from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from audit.models import log
from beregning.engine import TRANSPORT_NAVNE, hhmm
from register.models import Borger, Transport

from . import services
from .importer import ImportFejl, laes_timefil
from .models import Beregningskoersel, Koersel, Linje, LinjeResultat

TRANSPORT_VALG = list(Transport.choices)


def _laast(request, koersel):
    if koersel.status == Koersel.Status.GODKENDT:
        messages.info(request, "Kørslen er godkendt og låst. Genåbn den på godkendelsessiden, hvis noget skal rettes.")
        return redirect("godkend", pk=koersel.pk)
    return None


def _kontekst(koersel, steg, **ekstra):
    return {"koersel": koersel, "steg": steg, **ekstra}


@login_required
def dashboard(request):
    if request.method == "POST":
        try:
            aar, maaned = request.POST.get("maaned", "").split("-")
            dato = date(int(aar), int(maaned), 1)
        except (ValueError, TypeError):
            messages.error(request, "Vælg en måned.")
            return redirect("dashboard")
        koersel, oprettet = Koersel.objects.get_or_create(maaned=dato, defaults={"oprettet_af": request.user})
        if oprettet:
            log(request.user, "Oprettede kørsel", koersel, koersel.navn)
        return redirect("upload", pk=koersel.pk)
    return render(
        request,
        "koersel/dashboard.html",
        {"koersler": Koersel.objects.all(), "standard_maaned": date.today().strftime("%Y-%m")},
    )


@login_required
def upload(request, pk):
    koersel = get_object_or_404(Koersel, pk=pk)
    if (svar := _laast(request, koersel)):
        return svar
    fejl = ""
    if request.method == "POST":
        fil = request.FILES.get("fil")
        if not fil:
            fejl = "Vælg en Excel-fil først."
        else:
            try:
                raekker = laes_timefil(fil)
            except ImportFejl as e:
                fejl = str(e)
            else:
                services.opret_linjer(koersel, raekker, fil.name, request.user)
                log(request.user, "Uploadede timefil", koersel, f"{fil.name}, {len(raekker)} rækker")
                return redirect("gennemse", pk=koersel.pk)
    return render(request, "koersel/upload.html", _kontekst(koersel, 1, fejl=fejl))


def _dec(værdi: str):
    try:
        v = Decimal(værdi.replace(",", "."))
    except (InvalidOperation, AttributeError):
        return None
    return v if v >= 0 else None


@login_required
def gennemse(request, pk):
    koersel = get_object_or_404(Koersel, pk=pk)
    if (svar := _laast(request, koersel)):
        return svar
    if not koersel.linjer.exists():
        return redirect("upload", pk=pk)
    ret = request.GET.get("ret") == "1"

    if request.method == "POST":
        handling = request.POST.get("handling")
        if handling == "afklar":
            linje = get_object_or_404(Linje, pk=request.POST.get("linje"), koersel=koersel)
            borger = Borger.objects.filter(pk=request.POST.get("borger"), aktiv=True).first()
            if borger is None:
                messages.error(request, "Vælg en borger i listen.")
            else:
                linje.saet_borger(borger)
                linje.save()
                log(request.user, "Afklarede navnematch", linje, f"'{linje.fil_navn}' -> {borger.navn}")
            return redirect("gennemse", pk=pk)
        if services.uafklarede(koersel).exists():
            messages.error(request, "Afklar først de rækker fra Punchly, der ikke er matchet.")
            return redirect("gennemse", pk=pk)
        if handling == "gem":
            fejl = []
            for linje in koersel.linjer.select_related("borger"):
                km = _dec(request.POST.get(f"afstand_{linje.pk}", ""))
                transport = request.POST.get(f"transport_{linje.pk}", "")
                if km is None or transport not in dict(TRANSPORT_VALG):
                    fejl.append(linje.borger.navn)
                    continue
                b = linje.borger
                ændret = []
                if b.afstand_km != km:
                    b.afstand_km = km
                    ændret.append("afstand")
                if b.transport != transport:
                    b.transport = transport
                    ændret.append("transport")
                    if transport != Transport.SELV:
                        b.zoner = None
                if ændret:
                    b.save()
                    log(request.user, "Ændrede borger fra gennemsyn", b, f"{b.navn}: {', '.join(ændret)}")
                if linje.transport != transport:
                    linje.transport = transport
                    if transport != Transport.SELV:
                        linje.zoner, linje.individuel, linje.dage = None, False, None
                    else:
                        linje.zoner = b.zoner
                linje.save()
            if fejl:
                messages.error(request, "Ret afstand og transport for: " + ", ".join(fejl))
                return redirect(f"{request.path}?ret=1")
            messages.success(request, "Ændringerne er gemt i borgerregistret.")
        return redirect("undtagelser", pk=pk)

    linjer = list(koersel.linjer.select_related("borger"))
    alle_borgere = list(Borger.objects.filter(aktiv=True))
    for l in linjer:
        l.valgmuligheder = [b for b in alle_borgere if b.pk in l.kandidat_ids] if l.kandidater else alle_borgere
    return render(
        request,
        "koersel/gennemse.html",
        _kontekst(
            koersel,
            2,
            linjer=linjer,
            uafklarede=[l for l in linjer if l.match_status != Linje.Match.MATCHET],
            ret=ret,
            transport_valg=TRANSPORT_VALG,
        ),
    )


def _status(fejl: list[str]) -> tuple[str, str]:
    if not fejl:
        return "Klar", "ok"
    tekst = fejl[0]
    for nøgle, kort, klasse in (
        ("Sats", "Mangler sats", "bad"),
        ("Transport mangler", "Mangler transport", "warn"),
        ("Zone mangler", "Mangler zone", "bad"),
        ("findes ikke", "Ugyldig zone", "bad"),
        ("Fremmødedage", "Mangler dage", "bad"),
        ("Individuel beregning kræver", "Ret transport", "bad"),
    ):
        if nøgle in tekst:
            return kort, klasse
    return "Mangler oplysninger", "bad"


def _laes_undtagelser(request, koersel):
    for linje in koersel.linjer.select_related("borger"):
        t = request.POST.get(f"t_{linje.pk}", "")
        linje.transport = t if t in dict(TRANSPORT_VALG) else ""
        z = request.POST.get(f"z_{linje.pk}", "")
        linje.zoner = int(z) if z.isdigit() else None
        linje.individuel = request.POST.get(f"i_{linje.pk}") == "on"
        d = request.POST.get(f"d_{linje.pk}", "")
        linje.dage = int(d) if d.isdigit() else None
        if linje.transport != Transport.SELV:
            linje.zoner, linje.individuel, linje.dage = None, False, None
        if not linje.individuel:
            linje.dage = None
        linje.save()


@login_required
def undtagelser(request, pk):
    koersel = get_object_or_404(Koersel, pk=pk)
    if (svar := _laast(request, koersel)):
        return svar
    if not koersel.linjer.exists():
        return redirect("upload", pk=pk)
    if services.uafklarede(koersel).exists():
        messages.error(request, "Afklar først de rækker fra Punchly, der ikke er matchet.")
        return redirect("gennemse", pk=pk)

    generelt: list[str] = []
    afvist = False
    if request.method == "POST":
        _laes_undtagelser(request, koersel)
        if request.POST.get("handling") == "beregn":
            try:
                beregning = services.koer_beregning(koersel, request.user)
            except services.BeregningsFejl as e:
                afvist = True
                generelt = e.generelt
                messages.error(request, "Beregningen blev ikke kørt, fordi nogle borgere mangler oplysninger.")
            else:
                messages.success(request, f"Beregningen er kørt. PDF-rapport {beregning.rapport_id} er oprettet.")
                return redirect("godkend", pk=pk)
        else:
            log(request.user, "Gemte undtagelser", koersel, koersel.navn)
            messages.success(request, "Kladden er gemt.")
            return redirect("undtagelser", pk=pk)

    try:
        fejl = services.valider_koersel(koersel)
    except services.BeregningsFejl as e:
        fejl, generelt = {}, generelt + e.generelt
    linjer = list(koersel.linjer.select_related("borger"))
    for l in linjer:
        l.fejl = fejl.get(l.pk, [])
        l.status_tekst, l.status_klasse = _status(l.fejl)
        l.sats_mangler = l.borger.sats is None or l.borger.sats <= 0
    return render(
        request,
        "koersel/undtagelser.html",
        _kontekst(
            koersel,
            3,
            linjer=linjer,
            zoner=services.tilgaengelige_zoner(koersel.maaned),
            transport_valg=TRANSPORT_VALG,
            klar=sum(1 for l in linjer if not l.fejl),
            generelt=generelt,
            afvist=afvist,
            foerste_mangler=next((l.pk for l in linjer if l.fejl), None),
        ),
    )


@login_required
def godkend(request, pk):
    koersel = get_object_or_404(Koersel, pk=pk)
    beregning = koersel.aktiv_beregning
    if beregning is None:
        messages.info(request, "Der er ikke kørt en beregning endnu.")
        return redirect("undtagelser", pk=pk)

    if request.method == "POST":
        if request.POST.get("handling") == "genaabn":
            if koersel.status == Koersel.Status.GODKENDT:
                koersel.status = Koersel.Status.BEREGNET
                koersel.save(update_fields=["status"])
                log(request.user, "Genåbnede godkendt kørsel", koersel, koersel.navn)
                messages.info(request, "Kørslen er genåbnet. Ret oplysningerne og kør en ny beregning, eller godkend igen.")
            return redirect("undtagelser", pk=pk)
        if koersel.status == Koersel.Status.GODKENDT:
            return redirect("godkend", pk=pk)
        resultat_id = request.POST.get("resultat")
        antal = services.godkend(beregning, request.user, int(resultat_id) if resultat_id else None)
        messages.success(request, f"{antal} borger(e) godkendt." if antal else "Intet at godkende.")
        return redirect("godkend", pk=pk)

    resultater = list(beregning.resultater.all())
    data = beregning.data
    for r in resultater:
        r.detaljer_data = data["linjer"][r.indeks]
        inp = r.detaljer_data["input"]
        r.transport_navn = TRANSPORT_NAVNE.get(inp["transport"], "-")
        r.timer_tekst = hhmm(inp["minutter"])
    return render(
        request,
        "koersel/godkend.html",
        _kontekst(
            koersel,
            4,
            beregning=beregning,
            resultater=resultater,
            kan_eksportere=services.kan_eksportere(koersel),
            historik=koersel.beregninger.select_related("bruger"),
        ),
    )


@login_required
def grundlag(request, pk, resultat):
    koersel = get_object_or_404(Koersel, pk=pk)
    beregning = koersel.aktiv_beregning
    if beregning is None:
        raise Http404
    r = get_object_or_404(beregning.resultater, pk=resultat)
    r.detaljer_data = r.detaljer
    inp = r.detaljer_data["input"]
    r.transport_navn = TRANSPORT_NAVNE.get(inp["transport"], "-")
    r.timer_tekst = hhmm(inp["minutter"])
    return render(request, "koersel/grundlag.html", {"koersel": koersel, "beregning": beregning, "r": r})


@login_required
def rapport(request, pk):
    beregning = get_object_or_404(Beregningskoersel, pk=pk)
    if not beregning.pdf:
        raise Http404
    log(request.user, "Åbnede PDF-rapport", beregning, beregning.rapport_id)
    return FileResponse(beregning.pdf.open("rb"), content_type="application/pdf", filename=f"beregning-{beregning.rapport_id}.pdf")


@login_required
def eksport(request, pk):
    koersel = get_object_or_404(Koersel, pk=pk)
    if not services.kan_eksportere(koersel):
        messages.error(request, "Lønudtrækket kan først eksporteres, når alle borgere er godkendt.")
        return redirect("godkend", pk=pk)
    beregning = koersel.aktiv_beregning
    log(request.user, "Eksporterede lønudtræk", beregning, beregning.rapport_id)
    svar = HttpResponse(services.lav_csv(beregning), content_type="text/csv; charset=utf-8")
    svar["Content-Disposition"] = f'attachment; filename="loenudtraek-{beregning.rapport_id}.csv"'
    return svar
