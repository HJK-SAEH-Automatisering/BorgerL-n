# BorgerLøn

Webapp, der erstatter Excel-arket "VIKA løn og kørsel": månedlig beregning af §103-arbejdsdusør
og §105-befordring for borgere i beskyttet beskæftigelse. Timefilen kommer fra Punchly.
Arkitektur, regler og begrundelser står i [docs/losningsforslag.md](docs/losningsforslag.md).

## Arbejdsgang

1. **Upload fra Punchly** – Excel-fil (.xlsx) med kolonnerne "Navn" og "Total timer (timer:minutter)".
   Skærmen viser, hvem der sidst uploadede en fil, og hvornår. Uploades en ny fil, erstattes
   rækkerne og rettelserne i de senere trin.
2. **Gennemse transport** – afstand og transport pr. borger. Rækker, der ikke kan matches på navn,
   afklares her. Rettelser gemmes i borgerregisteret.
3. **Undtagelser** – transport, zoner og individuel beregning for måneden, med statuslinje.
   Mangler en borger oplysninger, når der trykkes "Beregn", rulles siden til den første række,
   der mangler noget, og rækken markeres.
4. **Godkend** – beregningsgrundlag pr. borger. Intet kan eksporteres, før alle er godkendt.

Hver gang der trykkes "Beregn", gemmes et uforanderligt snapshot og en PDF-rapport, der
specificerer udregningen for hver borger (uden CPR og adresse). Gamle rapporter slettes aldrig.

## Kom i gang (Windows)

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py seed_demo      # fiktive borgere, en demobruger og eksempel/punchly-eksempel.xlsx
.venv/Scripts/python manage.py runserver
```

Åbn http://localhost:8000. `seed_demo` udskriver adgangskoden til demobrugeren én gang. Opret
rigtige brugere med `manage.py createsuperuser` eller i admin. Zonepriser (NT, gældende fra
21.01.2025) og parametre (30 % egenbetaling, 10 km) lægges ind af migreringen og redigeres under
"Stamdata og log" (Django admin).

## Database

SQLite (`db.sqlite3`) bruges som standard. Til produktion med MSSQL:

```bash
.venv/Scripts/python -m pip install -r requirements-mssql.txt
```

og sæt miljøvariablerne `DB_ENGINE=mssql`, `DB_NAME`, `DB_HOST`, `DB_USER`, `DB_PASSWORD` (valgfrit:
`DB_PORT`, `DB_DRIVER`, `DB_EXTRA_PARAMS`), kør derefter `manage.py migrate`. MSSQL-opsætningen
er endnu ikke afprøvet mod en rigtig server.

Øvrige miljøvariabler: `DJANGO_DEBUG` (sæt til `0` i drift), `DJANGO_SECRET_KEY` (påkrævet, når
debug er slået fra), `DJANGO_ALLOWED_HOSTS`, `MEDIA_ROOT` (hvor PDF-rapporterne gemmes), `SQLITE_PATH`.

## Test og kontrol

```bash
.venv/Scripts/python manage.py test
.venv/Scripts/python manage.py verificer_rapport 2026-10-001
```

`verificer_rapport` kontrollerer, at den gemte PDF er uændret (SHA-256). Den gemte PDF er selve
beviset. En genskabt PDF er kun byte-identisk, så længe rapportens layout (`LAYOUT_VERSION` i
`beregning/pdf.py`) er uændret.

## Struktur

- `beregning/` – beregningsmotor (ren Python) og PDF-rapport
- `register/` – borgerregister (CPR vises maskeret, visning logges)
- `stamdata/` – zonepriser og parametre
- `koersel/` – månedlig kørsel: import, de fire skærme, godkendelse og eksport
- `audit/` – auditlog
