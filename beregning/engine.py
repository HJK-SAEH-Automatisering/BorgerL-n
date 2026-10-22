"""Beregningsmotor for arbejdsdusør (§103 SEL) og befordring (§105 SEL).

Ren Python uden Django-afhængighed. Reglerne er udledt af formlerne i arket
"VIKA løn og kørsel" (fanebladet "Indberetningsliste") og er beskrevet i
docs/losningsforslag.md. Hver beregning returnerer både beløb og et trin-for-trin
beregningsgrundlag, som vises ved godkendelse og skrives i PDF-rapporten.
"""

from dataclasses import dataclass, field
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

ORE = Decimal("0.01")
KRONER = Decimal("1")

TRANSPORT_SELV = "selv"
TRANSPORT_TAXA = "taxa"
TRANSPORT_INGEN = "ingen"
TRANSPORT_NAVNE = {TRANSPORT_SELV: "Kører selv", TRANSPORT_TAXA: "Taxa", TRANSPORT_INGEN: "Ingen udgift"}


def kr(v: Decimal) -> str:
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tal(v: Decimal, decimaler: int = 1) -> str:
    return f"{v:,.{decimaler}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def hhmm(minutter: int) -> str:
    return f"{minutter // 60}:{minutter % 60:02d}"


@dataclass(frozen=True)
class Parametre:
    max_egenbetaling_procent: Decimal
    afstandskrav_km: Decimal
    grundtakst: Decimal
    grundtakst_zoner: int = 2


@dataclass(frozen=True)
class Zonepris:
    kontant_barn: Decimal
    pendler_barn: Decimal


@dataclass
class Input:
    navn: str
    minutter: int | None
    sats: Decimal | None
    traek_procent: Decimal
    transport: str
    zoner: int | None = None
    individuel: bool = False
    dage: int | None = None
    afstand_km: Decimal = Decimal("0")
    tj_nr: str | None = None
    dobbelt: bool = False


@dataclass
class Resultat:
    fejl: list[str] = field(default_factory=list)
    advarsler: list[str] = field(default_factory=list)
    loen_foer: Decimal = Decimal("0")
    skattetraek: Decimal = Decimal("0")
    loen_efter: Decimal = Decimal("0")
    egenbetaling: Decimal = Decimal("0")
    traek_991: Decimal = Decimal("0")
    udbetaling_991: Decimal = Decimal("0")
    grundlag: list[dict] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.fejl

    def til_dict(self) -> dict:
        return {
            "fejl": self.fejl,
            "advarsler": self.advarsler,
            "loen_foer": str(self.loen_foer),
            "skattetraek": str(self.skattetraek),
            "loen_efter": str(self.loen_efter),
            "egenbetaling": str(self.egenbetaling),
            "traek_991": str(self.traek_991),
            "udbetaling_991": str(self.udbetaling_991),
            "grundlag": self.grundlag,
        }


def valider(inp: Input, zonepriser: dict[int, Zonepris]) -> list[str]:
    fejl: list[str] = []
    if inp.minutter is None or inp.minutter < 0:
        fejl.append("Timer mangler eller er ugyldige.")
    if inp.sats is None or inp.sats <= 0:
        fejl.append("Sats pr. time mangler på borgeren.")
    if inp.transport not in TRANSPORT_NAVNE:
        fejl.append("Transport mangler.")
        return fejl
    if inp.individuel and inp.transport != TRANSPORT_SELV:
        fejl.append("Individuel beregning kræver, at transporten er 'Kører selv'.")
    if inp.transport == TRANSPORT_SELV:
        if inp.zoner is None:
            fejl.append("Zone mangler.")
        elif inp.zoner not in zonepriser:
            fejl.append(f"Zone {inp.zoner} findes ikke i zonetabellen.")
    if inp.individuel and not (inp.dage is not None and 1 <= inp.dage <= 31):
        fejl.append("Fremmødedage mangler (1-31).")
    return fejl


def _trin(res: Resultat, titel: str, formel: str, indsat: str, resultat: str, note: str = "") -> None:
    res.grundlag.append(
        {"nr": len(res.grundlag) + 1, "titel": titel, "formel": formel, "indsat": indsat, "resultat": resultat, "note": note}
    )


def beregn(inp: Input, par: Parametre, zonepriser: dict[int, Zonepris]) -> Resultat:
    res = Resultat()
    res.fejl = valider(inp, zonepriser)
    if res.fejl:
        return res

    timer = Decimal(inp.minutter) / Decimal(60)
    _trin(
        res,
        "Timer fra Punchly",
        "timer:minutter omregnes til decimaltimer",
        f"{hhmm(inp.minutter)} = {inp.minutter} min / 60",
        f"{tal(timer, 2)} timer",
    )

    res.loen_foer = (Decimal(inp.minutter) * inp.sats / Decimal(60)).quantize(ORE, ROUND_HALF_UP)
    _trin(
        res,
        "Løn før skat (lønart 110)",
        "minutter x sats / 60, afrundet til øre",
        f"{inp.minutter} min x {kr(inp.sats)} kr / 60",
        f"{kr(res.loen_foer)} kr",
    )

    res.skattetraek = (res.loen_foer * inp.traek_procent / Decimal(100)).quantize(KRONER, ROUND_DOWN)
    _trin(
        res,
        "Skattetræk",
        "løn før skat x trækprocent, nedrundet til hele kroner",
        f"{kr(res.loen_foer)} kr x {tal(inp.traek_procent)} %",
        f"{kr(res.skattetraek)} kr",
    )

    res.loen_efter = res.loen_foer - res.skattetraek
    _trin(
        res,
        "Løn efter skat",
        "løn før skat - skattetræk",
        f"{kr(res.loen_foer)} kr - {kr(res.skattetraek)} kr",
        f"{kr(res.loen_efter)} kr",
    )

    maks_andel = (res.loen_efter * par.max_egenbetaling_procent / Decimal(100)).quantize(ORE, ROUND_DOWN)
    res.egenbetaling = min(maks_andel, par.grundtakst)
    _trin(
        res,
        "Borgerens egenbetaling for transport",
        f"mindste af {tal(par.max_egenbetaling_procent, 0)} % af løn efter skat og grundtakst for {par.grundtakst_zoner} zoner",
        f"min({kr(res.loen_efter)} kr x {tal(par.max_egenbetaling_procent, 0)} % = {kr(maks_andel)} kr ; grundtakst {kr(par.grundtakst)} kr)",
        f"{kr(res.egenbetaling)} kr",
        "Borgeren betaler selv inden for 10 km / 2 zoner, dog aldrig mere end 30 % af løn efter skat (§105 SEL).",
    )

    if inp.transport == TRANSPORT_INGEN:
        _trin(res, "Transport: ingen udgift", "ingen træk og ingen udbetaling", "-", "0,00 kr")
    elif inp.transport == TRANSPORT_TAXA:
        res.traek_991 = res.egenbetaling
        _trin(
            res,
            "Taxa: egenbetaling trækkes (lønart 991)",
            "kommunen betaler taxaen, borgerens egenbetaling trækkes i lønnen",
            f"egenbetaling {kr(res.egenbetaling)} kr",
            f"træk {kr(res.traek_991)} kr",
        )
    elif inp.minutter == 0:
        _trin(res, "Ingen timer, ingen udbetaling", "udbetaling af kørsel kræver timer", "0:00 timer", "0,00 kr")
    elif inp.individuel:
        pris = zonepriser[inp.zoner]
        brutto = Decimal(2) * pris.kontant_barn * Decimal(inp.dage)
        res.udbetaling_991 = max(brutto - res.egenbetaling, Decimal("0")).quantize(ORE)
        _trin(
            res,
            "Individuel beregning: transportudgift for måneden",
            "2 x kontantpris barn/67 for zonen x fremmødedage",
            f"2 x {kr(pris.kontant_barn)} kr x {inp.dage} dage ({inp.zoner} zoner)",
            f"{kr(brutto)} kr",
        )
        _trin(
            res,
            "Kommunens udbetaling (lønart 991)",
            "transportudgift for måneden - egenbetaling, mindst 0",
            f"{kr(brutto)} kr - {kr(res.egenbetaling)} kr",
            f"{kr(res.udbetaling_991)} kr",
        )
    else:
        pris = zonepriser[inp.zoner]
        res.udbetaling_991 = max(pris.pendler_barn - res.egenbetaling, Decimal("0")).quantize(ORE)
        _trin(
            res,
            f"Zonepris for {inp.zoner} zoner",
            "pendlerkort barn/67 fra zonetabellen",
            f"{inp.zoner} zoner",
            f"{kr(pris.pendler_barn)} kr",
        )
        _trin(
            res,
            "Kommunens udbetaling (lønart 991)",
            "zonepris - egenbetaling, mindst 0",
            f"{kr(pris.pendler_barn)} kr - {kr(res.egenbetaling)} kr",
            f"{kr(res.udbetaling_991)} kr",
        )

    if inp.dobbelt:
        res.advarsler.append("Samme navn forekommer flere gange i filen (mulig dobbeltansættelse).")
    if inp.minutter == 0:
        res.advarsler.append("Ingen timer registreret i perioden.")
    if inp.transport == TRANSPORT_SELV and inp.zoner is not None:
        if inp.afstand_km > par.afstandskrav_km and inp.zoner <= par.grundtakst_zoner:
            res.advarsler.append(
                f"Afstanden er {tal(inp.afstand_km)} km (over {tal(par.afstandskrav_km, 0)} km), men der er kun valgt {inp.zoner} zoner."
            )
        if inp.afstand_km <= par.afstandskrav_km and inp.zoner > par.grundtakst_zoner:
            res.advarsler.append(
                f"Afstanden er {tal(inp.afstand_km)} km (højst {tal(par.afstandskrav_km, 0)} km), men der er valgt {inp.zoner} zoner."
            )
    return res
