---
nummer: task-0014
titel: Reparationsscript, der gendanner pakker i .venv, som sikkerhedstjenesten har sat i karantæne
kilde: interview
status: afsluttet
oprettet: 2026-10-27
---

# task-0014 — Reparationsscript, der gendanner pakker i .venv, som sikkerhedstjenesten har sat i karantæne

## Hvad og hvorfor
En sikkerhedstjeneste på maskinen har seks gange erstattet filen `django/utils/cache.py` i `.venv` med en tekstfil, `cache.py.txt`, så Django ikke kan starte. Årsagen kan ikke fjernes: administratoren kan ikke undtage filen, projektet skal blive i OneDrive, og `.venv` skal blive i projektmappen. Hver gang er løsningen at slette `.venv` og bygge den forfra. Opgaven laver et lille script, der finder en erstattet fil og gendanner den pakke, den hører til, med én kommando, uden at bygge hele miljøet forfra.

Scriptet omgår ikke sikkerhedstjenesten og ændrer ikke på, hvad den gør. Det geninstallerer bare standardpakken. Filen går sandsynligvis i karantæne igen efter nogle timer, og så køres scriptet igen.

## Færdig når
- [ ] Én kommando kører scriptet fra projektmappen i PowerShell, og den virker også, når Django ikke kan startes. Scriptet bruger kun Pythons standardbibliotek og ikke Django.
- [ ] Er miljøet i orden, siger scriptet det og ændrer ingenting.
- [ ] Findes der filer i pakkerne i `.venv`, som er erstattet af en karantænetekst (en fil med endelsen `.py.txt`, hvis indhold begynder med teksten om, at filen er sat i karantæne), melder scriptet hvilke pakker det drejer sig om og gendanner dem.
- [ ] En pakke gendannes til samme udgave, som er installeret, uden at røre andre pakker og uden at slette eller bygge `.venv` forfra.
- [ ] Efter en reparation kontrollerer scriptet, at Django kan importeres, og siger resultatet. Mislykkes det, siger scriptet hvad der er galt, og afslutter med en fejlkode.
- [ ] Der er en tilstand, der kun tjekker og melder, uden at ændre noget.
- [ ] Meddelelserne er på dansk og i almindeligt sprog. Der skrives ingen hemmeligheder eller adgangskoder.
- [ ] Scriptet ændrer ikke på selve karantænefilen på andre måder end at gendanne pakken, og det forsøger ikke at skjule, ændre eller omgå sikkerhedstjenestens arbejde.
- [ ] `README.md` og `CLAUDE.md` nævner kort kommandoen og hvornår den bruges: når Django pludselig ikke starter, fx med "No module named 'django.utils.cache'".
- [ ] Der er tests, der viser, at et sundt miljø ikke ændres, at en karantæneerstattet fil findes og melder pakken, at tjek-tilstanden ikke ændrer noget, og at gendannelsen kaldes for netop den pakke. Testene bruger en midlertidig mappe med opdigtede filer og laver ikke et rigtigt kald til pakkeregistret.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- **Standardbiblioteket.** Scriptet er en Python-fil, fx `scripts/reparer_miljo.py`, som kun bruger standardbiblioteket. Så virker det, selv når Django er i stykker, og det kræver ingen scriptrettigheder i PowerShell. Kommandoen er `.venv\Scripts\python.exe scripts\reparer_miljo.py`, og med et flag til tjek-tilstand.
- **Find karantæne.** Scriptet leder gennem pakkemappen i `.venv` efter filer med endelsen `.py.txt`, hvor indholdet begynder med teksten om karantæne. Pakken er den øverste mappe eller det øverste modul i pakkemappen. Pakkens udgave læses fra dens installationsoplysninger.
- **Gendan.** Pakken geninstalleres med pakkehåndtereren i `.venv`, for præcis den udgave, uden at røre afhængigheder og uden at hente andet (`--force-reinstall --no-deps` på `pakke==udgave`). Pakkehåndtereren er den eneste del, der bruger netværket.
- **Kontrol.** Til sidst forsøger scriptet at importere Django med miljøets Python og melder resultatet.
- **Tests.** Funktionerne, der finder karantænefiler og bygger kommandoen til gendannelsen, er adskilt fra selve kaldet til pakkehåndtereren, så de kan prøves uden netværk. Testene kan køres med Djangos testkører, og hvis Django ikke kan startes, kan de køres direkte med `python -m unittest`.
- **Dokumenter.** Kommandoen står under "Til dig, der driver den" i README og under Kommandoer i CLAUDE.md.

## Hvad vi ikke rører
- Appens kode, Django og alle andre pakker.
- `.claude/launch.json` og hvordan serveren startes.
- Sikkerhedstjenesten og dens indstillinger. Scriptet forsøger ikke at skjule, undtage eller omgå noget.
- Hvor `.venv` ligger, og hvordan den normalt bygges.

## Afhænger af
task-0013 — den er bygget og venter på menneskets godkendelse. Der bygges kun på én opgave ad gangen, og denne sendes først af sted, når task-0013 er afsluttet og flettet.

## Beslutninger
- BESLUTTET: Et Python-script med standardbiblioteket, ikke et PowerShell-script — det virker, selv når Django er i stykker, kræver ingen scriptrettigheder og kan testes. Afvist: et PowerShell-script.
- BESLUTTET: Scriptet gendanner kun den pakke, der er ramt, til samme udgave — hurtigere og mere forudsigeligt end at bygge hele `.venv` forfra. Afvist: at slette og bygge `.venv`.
- BESLUTTET: Scriptet løser symptomet, ikke årsagen — årsagen kan hverken fjernes ved en undtagelse eller ved at flytte `.venv` eller projektet, og mennesket har afvist at rette i Djangos fil. Hvis filen går i karantæne igen, køres scriptet igen.
- BESLUTTET: Scriptet er ikke en del af serverens opstart — det køres, når nogen ser fejlen. Afvist: at ændre opstarten til at køre scriptet automatisk, som ville skjule at noget er galt.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
- `scripts/reparer_miljo.py`: scriptet, kun standardbiblioteket. Kommando fra projektmappen:
  `.venv\Scripts\python.exe scripts\reparer_miljo.py`. Tjek-tilstand: `--tjek`. `.venv` findes fra scriptets egen placering (projektroden), ikke arbejdsmappen. (Færdig når 1, 6)
  - Leder gennem site-packages efter `*.py.txt`, hvis første bytes (op til 512, med BOM håndteret for UTF-8 og UTF-16) er karantænebeskeden. (Færdig når 3)
  - Pakke og udgave slås op via `*.dist-info`: først filens sti i RECORD, ellers øverste mappe/modul mod top_level.txt og RECORD. Navn og udgave fra METADATA. (Færdig når 3, 4)
  - Gendannelse: `[venv-python, -m, pip, install, --force-reinstall, --no-deps, pakke==udgave]` via subprocess uden shell, én gang pr. pakke. Returkoden tjekkes. (Færdig når 4)
  - Kontrol til sidst: `venv-python -I -c "import django, django.utils.cache"`, resultatet meldes. Mislykkes det, meldes den sidste fejllinje, og returkoden er 2. (Færdig når 5)
  - Sundt miljø: melder "i orden" og afslutter med 0 uden at ændre noget. (Færdig når 2)
  - Meddelelser på dansk, kun pakkenavne, udgaver og stier i site-packages. Slutmeldingen efter en reparation siger, at filen kan blive sat i karantæne igen, og at scriptet så køres igen. (Færdig når 7)
  - Karantænefilerne røres ikke; scriptet sletter, omdøber eller skriver ingen filer selv. (Færdig når 8)
  - Opdelt til test: `find_quarantine_files(mappe)`, `determine_package(mappe, fil)`, `build_restore_command(python, pakke)`, `run_command(kommando)` (selve kaldet; injiceres som `runner` i `main`), `check_import` (injiceres som `importer`).
- `scripts/test_reparer_miljo.py` (23 tests, opdigtet mappe og dist-info, intet kald til pip): sundt miljø ændres ikke og melder det; karantænefil findes (også med BOM og UTF-16) og pakken meldes; `.py.txt` uden karantænetekst og andre filer med teksten ignoreres; tjek-tilstanden ændrer intet; kommandoen bygges for netop pakke og udgave; fejl i pip, import eller ukendt pakke giver fejlkode. (Færdig når 10)
- `scripts/__init__.py`: tom fil, så `manage.py test` finder testene i `scripts/`. Det er den eneste ændring, der skulle til for at få dem med i Djangos testkørsel; selve testkørslen er uændret.
- `README.md`: nyt afsnit "Når appen pludselig ikke starter" under "Til dig, der driver den", med kommandoen og `--tjek`. Rettet efter udtrykkelig besked fra architect om at gøre det. (Færdig når 9)
- `CLAUDE.md`: tre linjer under Kommandoer (kommandoen, `--tjek`, unittest-kørslen), et kort afsnit om scriptet og en række i strukturtabellen. (Færdig når 9)

Returkoder (mit valg, som du bad mig skrive): 0 = i orden eller gendannet; 1 = `--tjek` fandt karantænefiler; 2 = fejl (pip mislykkedes, Django kan ikke importeres efter reparationen eller i et ellers sundt miljø, filen hører til en pakke, der ikke kan bestemmes, eller `.venv` mangler). Tjek-tilstand med en ubestemmelig pakke giver også 2.

Sådan køres testene: `.venv\Scripts\python.exe -m unittest scripts.test_reparer_miljo` (virker uden Django), og de indgår i `.venv\Scripts\python.exe manage.py test` (Django finder dem på grund af `scripts/__init__.py`).

Kørt:
- `manage.py test`: "Ran 123 tests ... OK" (heri de 23 nye; `manage.py test scripts` alene: "Found 23 test(s) ... OK").
- `python -m unittest scripts.test_reparer_miljo`: "Ran 23 tests ... OK".
- `makemigrations --check`: "No changes detected".
- `scripts\reparer_miljo.py --tjek` mod den rigtige `.venv`: "Ingen filer er sat i karantæne i .venv. Django kan importeres. Miljøet er i orden. Intet er ændret." Returkode 0. Scriptet er ikke kørt i gendanne-tilstand mod den rigtige `.venv`, og der er ikke oprettet karantænefiler i den. Ingen spærring eller karantæne mødt.

### Hvad er ikke lavet, og hvorfor
- Selve gendannelsen mod et rigtigt pakkeregister (pip) er ikke afprøvet; det måtte jeg ikke mod den rigtige `.venv`, og testene kalder ikke pip. Kommandoen er kun prøvet som liste i en test.
- Linteren er ikke sat op i projektet; ikke kørt.

### Uklart
- **Gammel karantænefil efter en reparation.** pip fjerner kun de filer, der står i RECORD; `cache.py.txt` står der ikke, så den ligger tilbage ved siden af den gendannede `cache.py`. Havde scriptet talt den med, ville den blive fundet igen og igen. Jeg har derfor valgt: en `.py.txt` med karantænetekst tæller kun som fund, hvis den originale `.py` ved siden af mangler. Det ændrer ikke filen (opgaven forbyder det), men er en fortolkning af "Find karantæne", som du bør bekræfte.
- **Hvis pip selv er sat i karantæne**, kan scriptet ikke gendanne den med pip (pip mangler). Scriptet melder da, at gendannelsen mislykkedes, og afslutter med 2. Det er ikke løst; det er et nyt behov, ikke noget jeg har bygget.
- **Status** er sat til `i-gang` i filens øverste linjer, som min rolle foreskriver. Den er ikke sat videre.
