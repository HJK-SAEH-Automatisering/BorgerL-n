---
nummer: test-0002
titel: Hele testsuiten på grenen task-0003-env-loading
status: behandlet
rolle: tester
oprettet: 2026-10-23
omfang: Hele suiten, migreringstjek og de fire første punkter i Færdig når for task-0003
---

# test-0002 — Hele testsuiten på grenen task-0003-env-loading

## Hvad blev prøvet
- `manage.py test` (alle apps) på grenen `task-0003-env-loading`: 58 tests, OK, ingen systemfejl.
- `manage.py test config -v 2`: de 7 tests i `config/tests.py` kører hver for sig og er grønne.
- `manage.py makemigrations --check`: "No changes detected".
- `git check-ignore -v .env`: ignoreret af `.gitignore` linje 227. `.env.example` er ikke ignoreret og er den eneste af de to som git sporer (`git ls-files`).
- `git diff main -- .env.example`: kun kommentarlinjerne øverst er ændret. Alle nøglelinjer er uændrede, ingen tilføjet eller fjernet.
- `requirements.txt` indeholder `python-dotenv>=1.0`.
- Læst `config/settings.py` og `config/tests.py` og holdt dem op mod de fire første punkter i Færdig når.
- Dækning af de fire første punkter i `config/tests.py`:
  - Punkt 1 (nøgler fra `.env` bruges): `test_noegler_fra_env_bruges`, inkl. kommentar og anførselstegn.
  - Punkt 2 (maskinen vinder): `test_maskinens_vaerdi_vinder_over_env`. Det tilhørende tomme tilfælde dækkes af `test_tom_vaerdi_i_env_overskriver_ikke_maskinens_vaerdi`.
  - Punkt 3 (mangler `.env`, ingen fejl og ingen meddelelse): `test_manglende_env_goer_ingenting` tjekker miljø, stdout og stderr.
  - Punkt 4 (`.env` ikke versionsstyret, samme nøgler): ingen test. Se F2.
  - Punkt 6 (tom nøgle behandles som ikke sat): `test_tom_vaerdi_i_env_behandles_som_ikke_sat` og `test_standardvaerdien_gaelder_naar_noeglen_er_tom_i_env`.
  - Stedet for søgningen (projektroden, ikke arbejdsmappen): `test_indstillingerne_soeger_env_i_projektroden_ikke_i_arbejdsmappen`.

## Hvad holdt
- Hele suiten er grøn, og migreringerne er i takt med modellerne. `.venv` virkede uden spærring eller karantæne.
- `load_env` gør det opgaven siger: maskinens værdi vinder, en tom værdi i filen sættes ikke, manglende fil giver ingen fejl og ingen udskrift.
- Testene gendanner miljøet efter sig (`mock.patch.dict`) og bruger opdigtede nøgler, så de ikke afhænger af eller skriver værdier fra et rigtigt miljø.
- `.env` er ignoreret, `.env.example` har samme nøgler som på `main`.
- Testresultatet er ikke påvirket af en lokal `.env`: der ligger ingen i projektroden (kun fil-eksistens tjekket, indholdet ikke læst).

## Hvad blev ikke prøvet
- At `manage.py runserver` faktisk henter en udfyldt `.env`. Det ville kræve en `.env` i projektroden, og den må jeg ikke oprette. Det positive led fra punkt 1 ("både lokalt og når testene køres") er derfor kun prøvet gennem `load_env`, ikke gennem selve indstillingerne.
- Kantværdier i selve `.env`-formatet (byte order mark, værdi med kun mellemrum, nøgle uden `=`): lille konsekvens, og formatet fortolkes af `python-dotenv`. Ikke prøvet.
- MSSQL-stien og produktionsindstillingerne (`DJANGO_DEBUG` slået fra uden `DJANGO_SECRET_KEY`): uden for opgavens omfang ("Hvad vi ikke rører").
- Intet rørt i `.venv`, ingen filer genskabt, ingen pakker installeret. Ingen browser startet.

## Fund

### F1 — Ingen test beviser at indstillingerne selv indlæser `BASE_DIR/.env` · alvor: note
**Reproduktion:** I `config/settings.py` står `load_env(BASE_DIR / ".env")`. Fjernes den linje, er alle 58 tests stadig grønne. Testen `test_indstillingerne_soeger_env_i_projektroden_ikke_i_arbejdsmappen` kører settings fra en anden arbejdsmappe og tjekker kun at nøglen *ikke* dukker op. Den består også uden kaldet. De øvrige seks tests kalder `load_env` direkte med en sti de selv har lavet.
**Hvorfor det betyder noget:** Punkt 1 lover at en `.env` i projektroden virker af sig selv, når appen køres og når testene køres. Det led der binder funktionen til indstillingerne og til den rigtige sti, er uprøvet. En senere ændring kan fjerne eller pege kaldet forkert uden at nogen test fejler. Konsekvensen er lille: appen kører bare som før, uden at brugeren får besked.
**Forslag:** En test der patcher `dotenv_values` eller `load_env` og kører settings (`runpy`), og som tjekker at kaldet sker med `BASE_DIR / ".env"`. Det kræver ikke en rigtig `.env`.

### F2 — Punkt 4 er ikke dækket af en kontrol · alvor: note
**Reproduktion:** Ingen test tjekker at `.env` er ignoreret af git, eller at `.env.example` har de samme nøgler som før. Jeg har efterprøvet begge dele manuelt (se Hvad blev prøvet), og de holder.
**Hvorfor det betyder noget:** Opgaven kræver tests for "de fire første punkter". Punkt 4 er en tilstand i repoet, ikke kode, og en test af det måler `.gitignore` og en nøgleliste frem for adfærd. Der er derfor en reel tvivl om, om punktet skal have en test. Fjernes `.env` fra `.gitignore`, opdager ingen kontrol det, og så kan en udfyldt `.env` blive committet. Den risiko er den alvorligste af de to fund, men hører mest hjemme i en gennemgang af `.gitignore`.
**Forslag:** Afgør om punkt 4 skal have en kontrol. Hvis ja, er det en opgave til `developer` (fx en test der kører `git check-ignore .env`). Hvis nej, så ret ordlyden i opgaven, så den kun kræver tests af de tre adfærdspunkter.

## Uklart
- Skal "tests for de fire første punkter" læses bogstaveligt, så punkt 4 også skal have en test? Jeg har antaget at det er et spørgsmål til `architect` og meldt det som F2.
- Opgavens developer-noter siger "Hele suiten ... kunne ikke køres denne gang" på grund af `django\utils\cache.py` omdøbt til `cache.py.txt`. Jeg mødte ikke fejlen: `.venv` er genopbygget, og suiten kører. Noten er forældet, men jeg har ikke rettet i den.

## Afledte numre
intet — begge fund er afvist; se beslutningsloggen.
