---
nummer: task-0014
titel: Reparationsscript, der gendanner pakker i .venv, som sikkerhedstjenesten har sat i karantæne
kilde: interview
status: planlagt
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
### Hvad er ikke lavet, og hvorfor
### Uklart
