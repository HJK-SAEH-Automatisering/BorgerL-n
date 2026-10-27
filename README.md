# MedarbejderLøn

Webapp, der erstatter Excel-arket "VIKA løn og kørsel". Den beregner hver måned arbejdsdusør
(§103) og befordring (§105) for medarbejdere i beskyttet beskæftigelse ud fra en timefil fra Punchly.

En administrativ medarbejder uploader filen, retter transport og undtagelser og godkender
beregningen for én medarbejder ad gangen. Intet bliver eksporteret, før alt er godkendt.

Mappen og repoet hedder stadig BorgerLøn. Det er kun navnet i appen, der er skiftet.

## Til dig, der bruger den

Adressen til appen får du af den, der driver den. Hver måned går du fire trin igennem.

1. **Upload.** Vælg måneden på forsiden, og upload timefilen fra Punchly. Det er en Excel-fil
   (.xlsx) med kolonnerne "Navn" og "Total timer (timer:minutter)". Har filen også kolonnen
   "Antal arbejdsdage" med den enkelte medarbejders fremmødedage, bruges tallet som forslag, når
   individuel beregning vælges. Skærmen viser, hvem der sidst uploadede en fil, og hvornår. Uploades en ny fil, erstattes rækkerne og dine rettelser i
   de senere trin. Har filen rækker med ugyldige timer, afvises hele filen. Ret den, og upload igen.
2. **Gennemse transport.** Her står afstand og transport for hver medarbejder i filen. Rækker, som
   appen ikke kan genkende på navn, afklarer du selv. Appen gætter aldrig. Ændrer du afstand
   eller transport her, bliver det gemt hos medarbejderen og gælder fra nu af.
3. **Undtagelser.** Her rettes transport, zoner og individuel beregning for denne måned. Det du
   retter her, gælder kun måneden. Felter, der ikke passer til den valgte transport, er slået
   fra. Vælger du individuel beregning, står antal fremmødedage udfyldt fra filen, hvis den har
   dem. Du kan rette tallet. Mangler en medarbejder oplysninger, når du trykker "Beregn", rulles siden til den første
   række, der mangler noget.
4. **Godkend.** Ud for hver medarbejder er der en knap, "Beregningsgrundlag", som åbner en side i en
   ny fane med udregningen trin for trin. Du kan godkende en ad gangen eller alle på én gang. Knapperne øverst står fra venstre:
   "Godkend alle", "Genåbn til rettelser", "Eksportér lønudtræk (CSV)" og "Åbn PDF-rapport".
   Eksport og PDF kan først bruges, når alle er godkendt. Skal noget rettes bagefter, trykker du på
   "Genåbn til rettelser". Så fjernes alle godkendelser, og du kan godkende igen eller rette
   oplysningerne under Undtagelser.

Hver gang du trykker "Beregn", gemmes en PDF-rapport med udregningen for hver medarbejder, uden
CPR-nummer og adresse. Rapporterne kan ikke ændres, og gamle rapporter slettes aldrig. Trykker
du "Beregn" igen, bortfalder de tidligere godkendelser. CPR-numre vises kun maskeret i appen.

## Til dig, der driver den

### Kom i gang (Windows)

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py seed_demo
.venv/Scripts/python manage.py runserver
```

`seed_demo` opretter fiktive medarbejdere, en demobruger og en eksempelfil med timer. Adgangskoden til
demobrugeren vises kun én gang, første gang kommandoen køres. Åbn derefter http://localhost:8000.
Rigtige brugere oprettes med `manage.py createsuperuser` eller i administrationssiden.
Zonepriser og parametre (30 % egenbetaling, 10 km) lægges ind ved opsætningen og rettes under
"Stamdata og log" i administrationssiden.

### Indstillinger

Appen læser sine indstillinger fra miljøvariabler. Nøglerne står i `.env.example`:
`DJANGO_DEBUG` (sæt til `0` i drift), `DJANGO_SECRET_KEY` (påkrævet, når debug er slået fra),
`DJANGO_ALLOWED_HOSTS`, `MEDIA_ROOT` (hvor PDF-rapporterne gemmes) og `SQLITE_PATH`.

De kan også stå i en fil, der hedder `.env`, i projektets rodmappe. Kopiér `.env.example` til
`.env`, og udfyld kun de nøgler, du bruger. Nøgler uden værdi ignoreres, og variabler, der er sat
på maskinen, vinder over filen. `.env` hører ikke i versionsstyringen.

### Database

Som standard bruges en SQLite-fil. Til drift med MSSQL installeres den ekstra pakke, og
databasen sættes op med nøglerne `DB_ENGINE=mssql`, `DB_NAME`, `DB_HOST`, `DB_USER` og
`DB_PASSWORD` (valgfrit: `DB_PORT`, `DB_DRIVER`, `DB_EXTRA_PARAMS`):

```bash
.venv/Scripts/python -m pip install -r requirements-mssql.txt
.venv/Scripts/python manage.py migrate
```

MSSQL er endnu ikke afprøvet mod en rigtig server.

### Kontrol af en gemt rapport

Den gemte PDF er selve beviset på en beregning. Den kan kontrolleres for ændringer med
`manage.py verificer_rapport` og rapportens nummer, fx `2026-10-001`.

## Læs mere

- [docs/losningsforslag.md](docs/losningsforslag.md): reglerne, designet og begrundelserne.
- [CLAUDE.md](CLAUDE.md): kommandoer og opbygning, til dem der skal rette i appen.
