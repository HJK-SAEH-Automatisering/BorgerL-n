"""Genererer PDF-rapporten for en beregningskørsel ud fra et snapshot (dict).

Rapporten bygges udelukkende af snapshotten, så den kan genskabes identisk senere.
CPR og adresse indgår bevidst ikke; borgere identificeres med navn og Tj.nr.
"""

from decimal import Decimal
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .engine import TRANSPORT_NAVNE, hhmm, kr, tal

LAYOUT_VERSION = 1  # skal øges, når rapportens layout ændres

KILDE_TEKST = {"fil": "Punchly-filen", "register": "Borgerregistret", "manuelt": "Rettet i denne kørsel", "-": "-"}

_styles = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=_styles["Heading1"], fontSize=18, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=_styles["Heading2"], fontSize=12, spaceBefore=10, spaceAfter=4)
TXT = ParagraphStyle("txt", parent=_styles["BodyText"], fontSize=9, leading=11)
SMALL = ParagraphStyle("small", parent=TXT, fontSize=8, leading=10)
ADV = ParagraphStyle("adv", parent=TXT, textColor=colors.HexColor("#8a5a00"))

GRAA = colors.HexColor("#f1efe8")
LINJE = colors.HexColor("#b4b2a9")


def _p(tekst, stil=SMALL):
    return Paragraph(escape(str(tekst)), stil)


def _tabel(rækker, kolonnebredder, header=True, ret_hojre=()):
    t = Table(rækker, colWidths=kolonnebredder, repeatRows=1 if header else 0)
    stil = [
        ("GRID", (0, 0), (-1, -1), 0.4, LINJE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    if header:
        stil.append(("BACKGROUND", (0, 0), (-1, 0), GRAA))
    for k in ret_hojre:
        stil.append(("ALIGN", (k, 0), (k, -1), "RIGHT"))
    t.setStyle(TableStyle(stil))
    return t


def _input_raekker(linje: dict):
    i, k = linje["input"], linje["kilder"]

    def kilde(felt):
        return KILDE_TEKST.get(k.get(felt, "-"), k.get(felt, "-"))

    raekker = [[_p("Felt"), _p("Værdi"), _p("Kilde")]]
    raekker.append([_p("Timer"), _p(f"{hhmm(i['minutter'])} ({tal(Decimal(i['minutter']) / 60, 2)} t)"), _p(kilde("timer"))])
    raekker.append([_p("Sats pr. time"), _p(f"{kr(Decimal(i['sats']))} kr"), _p(kilde("sats"))])
    raekker.append([_p("Trækprocent"), _p(f"{tal(Decimal(i['traek_procent']))} %"), _p(kilde("traek_procent"))])
    raekker.append([_p("Afstand til arbejdssted"), _p(f"{tal(Decimal(i['afstand_km']))} km"), _p(kilde("afstand_km"))])
    raekker.append([_p("Transport"), _p(TRANSPORT_NAVNE.get(i["transport"], i["transport"])), _p(kilde("transport"))])
    raekker.append([_p("Zoner"), _p(i["zoner"] if i["zoner"] is not None else "-"), _p(kilde("zoner"))])
    raekker.append([_p("Individuel beregning"), _p("Ja" if i["individuel"] else "Nej"), _p(kilde("individuel"))])
    if i["individuel"]:
        raekker.append([_p("Fremmødedage"), _p(i["dage"]), _p(kilde("dage"))])
    return raekker


def _linje_blok(linje: dict):
    titel = f"{linje['navn']}" + (f" (Tj.nr. {linje['tj_nr']})" if linje["tj_nr"] else "")
    if linje["afdeling"]:
        titel += f" - {linje['afdeling']}"
    dele = [Paragraph(escape(titel), H2)]
    dele.append(_tabel(_input_raekker(linje), [50 * mm, 70 * mm, 50 * mm]))
    dele.append(Spacer(1, 4))
    trin = [[_p("Nr."), _p("Trin"), _p("Formel"), _p("Indsat"), _p("Resultat")]]
    for t in linje["grundlag"]:
        trin.append([_p(t["nr"]), _p(t["titel"]), _p(t["formel"]), _p(t["indsat"]), _p(t["resultat"])])
        if t.get("note"):
            trin.append([_p(""), Paragraph(f"<i>{escape(t['note'])}</i>", SMALL), "", "", ""])
    tabel = _tabel(trin, [9 * mm, 40 * mm, 50 * mm, 49 * mm, 22 * mm], ret_hojre=(4,))
    stil = []
    for r, raekke in enumerate(trin):
        if r and raekke[2] == "" and raekke[1] != "":
            stil += [("SPAN", (1, r), (4, r))]
    tabel.setStyle(TableStyle(stil))
    dele.append(tabel)
    res = linje["resultat"]
    dele.append(Spacer(1, 3))
    dele.append(
        _tabel(
            [
                [_p("Løn før skat"), _p("Løn efter skat"), _p("Træk (lønart 991)"), _p("Udbetaling (lønart 991)")],
                [
                    _p(f"{kr(Decimal(res['loen_foer']))} kr"),
                    _p(f"{kr(Decimal(res['loen_efter']))} kr"),
                    _p(f"{kr(Decimal(res['traek_991']))} kr"),
                    _p(f"{kr(Decimal(res['udbetaling_991']))} kr"),
                ],
            ],
            [42.5 * mm] * 4,
        )
    )
    for a in linje["advarsler"]:
        dele.append(Paragraph("Advarsel: " + escape(a), ADV))
    return KeepTogether(dele)


def _sidefod(rapport_id):
    def tegn(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(20 * mm, 10 * mm, f"Beregningsrapport {rapport_id}")
        canvas.drawRightString(190 * mm, 10 * mm, f"Side {doc.page}")
        canvas.restoreState()

    return tegn


def lav_rapport(d: dict) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"Beregningsrapport {d['rapport_id']}",
        author="BorgerLøn",
        invariant=1,
    )
    t, par = d["totaler"], d["parametre"]
    ind = [
        Paragraph(f"Beregningsrapport - løn og kørsel, {escape(d['maaned_tekst'])}", H1),
        Paragraph(
            "Rapporten specificerer, hvordan løn og befordring er beregnet for hver borger. "
            "Den er oprettet automatisk ved beregningen og kan ikke ændres bagefter.",
            TXT,
        ),
        Spacer(1, 6),
        _tabel(
            [
                [_p("Rapport-id"), _p(d["rapport_id"])],
                [_p("Beregnet"), _p(d["tidspunkt_tekst"])],
                [_p("Kørt af"), _p(d["bruger"])],
                [_p("Timefil fra Punchly"), _p(d["filnavn"] or "-")],
                [_p("Antal borgere"), _p(t["antal"])],
                [_p("Sum løn før skat"), _p(f"{kr(Decimal(t['loen_foer']))} kr")],
                [_p("Sum løn efter skat"), _p(f"{kr(Decimal(t['loen_efter']))} kr")],
                [_p("Sum træk (lønart 991)"), _p(f"{kr(Decimal(t['traek_991']))} kr")],
                [_p("Sum udbetaling (lønart 991)"), _p(f"{kr(Decimal(t['udbetaling_991']))} kr")],
            ],
            [60 * mm, 110 * mm],
            header=False,
        ),
        Paragraph("Anvendte parametre", H2),
        _tabel(
            [
                [_p("Parameter"), _p("Værdi")],
                [_p("Maksimal egenbetaling af løn efter skat"), _p(f"{tal(Decimal(par['max_egenbetaling_procent']), 0)} %")],
                [_p("Afstandskrav (egenbetaling inden for)"), _p(f"{tal(Decimal(par['afstandskrav_km']), 0)} km")],
                [
                    _p(f"Grundtakst for {par['grundtakst_zoner']} zoner (pendlerkort barn/67)"),
                    _p(f"{kr(Decimal(par['grundtakst']))} kr"),
                ],
                [_p("Zoneprisliste gældende fra"), _p(par["zonepriser_gyldig_fra"])],
            ],
            [110 * mm, 60 * mm],
        ),
    ]
    zr = [[_p("Zoner"), _p("Kontantbillet barn/67"), _p("Pendlerkort barn/67")]]
    for z, p in sorted(d["zonepriser"].items(), key=lambda kv: int(kv[0])):
        zr.append([_p(z), _p(f"{kr(Decimal(p['kontant_barn']))} kr"), _p(f"{kr(Decimal(p['pendler_barn']))} kr")])
    ind += [Paragraph("Anvendte zonepriser", H2), _tabel(zr, [30 * mm, 70 * mm, 70 * mm])]
    ind.append(Spacer(1, 8))
    for linje in d["linjer"]:
        ind.append(_linje_blok(linje))
    doc.build(ind, onFirstPage=_sidefod(d["rapport_id"]), onLaterPages=_sidefod(d["rapport_id"]))
    return buf.getvalue()
