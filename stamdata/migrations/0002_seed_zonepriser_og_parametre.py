from datetime import date
from decimal import Decimal

from django.db import migrations

# Antal zoner, kontant voksen, kontant barn/67, pendlerkort voksen, pendlerkort barn/67, rejsekort.
# Kilde: fanebladet "Zone priser" i "VIKA løn og kørsel.xlsx" (NT-priser gældende fra 21.01.2025).
ZONEPRISER = [
    (2, 24, 12, 435, "217.5", 23), (3, 34, 17, 585, "292.5", "32.8"), (4, 44, 22, 780, 390, "42.4"),
    (5, 54, 27, 960, 480, "51.6"), (6, 64, 32, 1140, 570, "60.8"), (7, 74, 37, 1320, 660, "70.3"),
    (8, 84, 42, 1470, 735, "79.8"), (9, 94, 47, 1650, 825, "89.3"), (10, 104, 52, 1800, 900, "98.8"),
    (11, 114, 57, 1950, 975, 109), (12, 120, 60, 2100, 1050, 114), (13, 130, 65, 2280, 1140, 124),
    (14, 140, 70, 2460, 1230, 133), (15, 150, 75, 2640, 1320, 143), (16, 160, 80, 2820, 1410, 152),
    (17, 170, 85, 2970, 1485, 162), (18, 180, 90, 3090, 1545, 171), (19, 190, 95, 3240, 1620, 181),
    (20, 200, 100, 3330, 1665, 190), (21, 210, 105, 3450, 1725, 200), (22, 220, 110, 3510, 1755, 209),
    (23, 230, 115, 3660, 1830, 219), (24, 240, 120, 3780, 1890, 228),
]
GYLDIG_FRA = date(2025, 1, 21)


def seed(apps, schema_editor):
    ZonePris = apps.get_model("stamdata", "ZonePris")
    Parameter = apps.get_model("stamdata", "Parameter")
    for zoner, kv, kb, pv, pb, rk in ZONEPRISER:
        ZonePris.objects.get_or_create(
            antal_zoner=zoner,
            gyldig_fra=GYLDIG_FRA,
            defaults=dict(
                kontant_voksen=Decimal(str(kv)), kontant_barn=Decimal(str(kb)),
                pendler_voksen=Decimal(str(pv)), pendler_barn=Decimal(str(pb)), rejsekort=Decimal(str(rk)),
            ),
        )
    Parameter.objects.get_or_create(
        noegle="max_egenbetaling_procent",
        gyldig_fra=date(2000, 1, 1),
        defaults=dict(vaerdi=Decimal("30"), beskrivelse="Borgerens egenbetaling for transport må højst udgøre denne procentdel af løn efter skat."),
    )
    Parameter.objects.get_or_create(
        noegle="afstandskrav_km",
        gyldig_fra=date(2000, 1, 1),
        defaults=dict(vaerdi=Decimal("10"), beskrivelse="Borgeren afholder selv transportudgifter inden for denne afstand (svarer til 2 zoner)."),
    )


class Migration(migrations.Migration):
    dependencies = [("stamdata", "0001_initial")]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
