# MedarbejderLøn

Webapp der erstatter Excel-arket "VIKA løn og kørsel". Den beregner hver måned §103-arbejdsdusør
og §105-befordring for medarbejdere i beskyttet beskæftigelse ud fra en timefil fra Punchly.
En administrativ medarbejder uploader filen, retter transport og undtagelser, og godkender
beregningen for én medarbejder ad gangen. Intet eksporteres før alt er godkendt.
Hver beregning gemmer et uforanderligt snapshot og en PDF-rapport (uden CPR og adresse).

Reglerne, designet og de uafklarede punkter står i `docs/losningsforslag.md`. Opstart for
mennesker står i `README.md`.

**Navnet:** appen hedder MedarbejderLøn i alt, hvad en bruger kan læse, og personerne hedder
"medarbejdere". Mappen og repoet hedder stadig BorgerLøn, og det gør navne i koden:
modellen `Borger`, tabellerne, skabelonfilerne `borger_*.html`, visningerne og adressenavnene
(`borger_liste` m.fl.), adressen `/borgere/` og feltnavnet `borger`. De er ikke omdøbt
(task-0007 ændrer kun den synlige tekst). Skriver du ny tekst til brugere, så brug "medarbejder".

## Stak

- Python 3.14, Django 6.1, `openpyxl` (import), `reportlab` (PDF). Afhængigheder: `requirements.txt`.
- Database: SQLite i udvikling og indtil webappen er godkendt. MSSQL i produktion via
  `mssql-django` (`requirements-mssql.txt`) — endnu ikke afprøvet mod en rigtig server.
- Virtuelt miljø: `.venv` i projektroden. Kald fortolkeren direkte.
- Server-renderede skabeloner med lidt vanilla JS. Ingen frontend-build.

## Kommandoer

```
.venv\Scripts\python.exe manage.py test
.venv\Scripts\python.exe manage.py runserver
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py makemigrations
.venv\Scripts\python.exe manage.py seed_demo
.venv\Scripts\python.exe manage.py verificer_rapport 2026-10-001
.venv\Scripts\python.exe scripts\reparer_miljo.py
.venv\Scripts\python.exe scripts\reparer_miljo.py --tjek
.venv\Scripts\python.exe -m unittest scripts.test_reparer_miljo
```

`reparer_miljo.py` geninstallerer pakker i `.venv`, hvis en sikkerhedstjeneste har erstattet en
fil med en karantænetekst (`*.py.txt`), så Django ikke starter. `--tjek` melder kun. Scriptet
bruger kun standardbiblioteket; dets tests kan også køres uden Django med den sidste linje.

`seed_demo` opretter fiktive medarbejdere, en demobruger og `eksempel/punchly-eksempel.xlsx`.
Byg, formatering og linter er ikke sat op.

Indstillinger læses fra processens miljøvariabler. En `.env` i projektroden indlæses automatisk
(`python-dotenv`, øverst i `config/settings.py`); maskinens egne variabler vinder over filen.
Nøglerne står i `.env.example`.

## Struktur

| Mappe | Indhold |
|---|---|
| `config/` | Indstillinger, URL'er |
| `beregning/` | `engine.py` (beregningsmotor, ren Python uden Django) og `pdf.py` (PDF-rapport bygget af et snapshot) |
| `register/` | Medarbejderregister: `Borger` (modellen hedder stadig sådan), `Afdeling`, formularer og skærme. CPR vises maskeret |
| `stamdata/` | `ZonePris` (versioneret pr. dato) og `Parameter`. Seedet af en migrering |
| `koersel/` | Månedlig kørsel: import, de fire skærme, `services.py`, godkendelse og CSV-eksport |
| `audit/` | `AuditLog` |
| `scripts/` | `reparer_miljo.py` (gendanner pakker i `.venv`, kun standardbiblioteket) og dets tests |
| `templates/`, `static/` | Skabeloner, CSS og JS |
| `docs/` | Dokumentation og rollernes papirspor |

## Domænebegreber

- **Punchly:** kildesystemet. Timefilen har kun navn og timer (t:mm), så rækker matches på navn.
  Usikre match afklares manuelt og gættes aldrig.
- **Tj.nr.:** medarbejderens interne nummer i registret. Står ikke i timefilen.
- **Lønart 110 og 991:** 110 er arbejdsdusør (løn før skat). 991 er kørsel: træk (taxa) eller
  udbetaling (kører selv).
- **Egenbetaling:** medarbejderen betaler selv transport inden for 10 km / 2 zoner, dog højst 30 % af
  løn efter skat. Kommunen betaler resten (zonepris minus egenbetaling).
- **Transport:** kører selv, taxa eller ingen udgift. **Individuel beregning** overstyrer
  standardberegningen for kører selv og bruger fremmødedage.
- **Zonepriser:** NT-takster, børne/67-taksten, ændres hvert år og er versioneret.
- **Beregningskørsel:** ét uforanderligt snapshot med PDF-rapport pr. gang "Beregn" trykkes.
  Godkendelse hører til en bestemt beregningskørsel. Kører man "Beregn" igen, bortfalder
  tidligere godkendelser.
- **Kørsel:** én måned. De fire trin: upload, gennemse transport, undtagelser, godkend.
