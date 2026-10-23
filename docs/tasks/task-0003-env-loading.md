---
nummer: task-0003
titel: Indlæs .env automatisk i indstillingerne
status: afsluttet
kilde: interview
oprettet: 2026-10-22
---

# task-0003 — Indlæs .env automatisk i indstillingerne

## Hvad og hvorfor
Appens indstillinger læses i dag kun fra maskinens miljøvariabler. Den der kører appen lokalt, skal derfor sætte hver nøgle i terminalen, før noget virker. `.env.example` lister nøglerne, men en udfyldt `.env` bliver ikke brugt. Opgaven får en udfyldt `.env` i projektroden til at virke af sig selv.

## Færdig når
- [ ] Ligger der en `.env` i projektroden, bruges dens nøgler som indstillinger, uden at de er sat på maskinen først. Det gælder både når appen køres lokalt, og når testene køres.
- [ ] Er en nøgle både sat på maskinen og står i `.env`, er det maskinens værdi, der gælder.
- [ ] Mangler `.env`, kører appen som i dag, uden fejl og uden meddelelse.
- [ ] `.env` versionsstyres ikke, og `.env.example` har de samme nøgler som før.
- [ ] Teksten i `.env.example`, der siger at `.env` ikke indlæses endnu, er rettet, og linjen i `CLAUDE.md` om indstillinger siger at `.env` indlæses automatisk.
- [ ] En nøgle der står tom i `.env` (fx `DJANGO_DEBUG=`), behandles som om den ikke var sat, så appens standardværdi gælder. Man kan derfor kopiere `.env.example` til `.env` og kun udfylde de nøgler man bruger.
- [ ] Der er tests for de fire første punkter.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- **Pakken `python-dotenv`.** Den tilføjes i `requirements.txt` med et versionsinterval i samme stil som de øvrige og installeres i `.venv`. Det er opgavens eneste nye afhængighed.
- **Ét sted.** Indlæsningen sker øverst i `config/settings.py`, før den første nøgle læses. `manage.py` og serveropstarten går begge gennem indstillingerne og rettes ikke.
- **Maskinen vinder.** Variabler der allerede er sat på maskinen, overskrives ikke af `.env`.
- **Filens sted.** `.env` søges i projektroden, ikke i den mappe man står i.
- **Tests.** Indlæsningen kan lægges i en lille funktion, så den kan prøves med en midlertidig fil. Metoden vælger udvikleren.
- Ingen standardværdier ændres. Værdierne i `.env` hører kun dér; ingen nøgle eller værdi skrives ind i kode, tests eller dokumenter ud over de nøglenavne der står i `.env.example`.

## Hvad vi ikke rører
- Hvilke nøgler der findes, og hvad de hedder.
- Valget mellem SQLite og MSSQL og alle databaseindstillinger.
- `manage.py` og `config/wsgi.py`.
- Reglerne for `DJANGO_DEBUG` og `DJANGO_SECRET_KEY`.
- Alt i `koersel`, `register`, `beregning`, `stamdata` og `audit`.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: `python-dotenv` frem for en egen indlæser — den er udbredt og håndterer anførselstegn og kommentarer rigtigt. Afvist: ti linjer egen kode, som skulle vedligeholdes. Besluttet af mennesket.
- BESLUTTET: Indlæsning øverst i `config/settings.py` — det er det ene sted alle indgange går igennem.
- BESLUTTET: Maskinens variabler vinder over `.env` — så en server kan sætte sine egne værdier uden at filen skal fjernes.
- BESLUTTET: En tom værdi i `.env` svarer til "ikke sat" — ellers ville en kopi af `.env.example` slå udviklingstilstanden fra og kræve en hemmelig nøgle. Afvist: at lade brugeren slette ubrugte nøgler. Besluttet af mennesket efter at udvikleren rejste spørgsmålet.
- BESLUTTET: Mangler `.env`, sker der intet — appen skal køre som i dag, hvor nøglerne kommer fra maskinen.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
- `requirements.txt`: `python-dotenv>=1.0` tilføjet og installeret i `.venv` (1.2.4). Ingen spærring.
- `config/settings.py`: funktionen `load_env(path)` øverst, kaldt med `BASE_DIR / ".env"` før den første nøgle læses. Bruger `load_dotenv(..., override=False)`, så maskinens variabler vinder. Mangler filen, sker intet (ingen fejl, ingen udskrift). Filen søges i projektroden, ikke arbejdsmappen. Punkt 1-3 i Færdig når.
- `config/tests.py` (ny): fire tests med en midlertidig fil og opdigtede nøgler (`BORGERLON_TEST_A`/`_B`): nøgler fra `.env` bruges; maskinens værdi vinder; manglende fil gør ingenting og skriver intet; indstillingerne henter ikke `.env` fra arbejdsmappen. Miljøet gendannes efter hver test. Punkt 6.
- `.env.example`: kommentaren øverst rettet, så den siger at `.env` indlæses automatisk og at maskinen vinder. Nøglerne er uændrede. `.env` var allerede i `.gitignore` (`.env`, `.env.*`, `!.env.example`); intet rettet der. Punkt 4 og 5.
- `CLAUDE.md`: linjen om indstillinger siger nu at en `.env` i projektroden indlæses automatisk, og at maskinen vinder. Punkt 5.
- Hele suiten kørt én gang: 55 tests, grøn. `makemigrations --check`: ingen ændringer. Punkt 7.
- Til README (architect): lokalt kan man nu lægge en `.env` i projektroden med nøglerne fra `.env.example` i stedet for at sætte dem i terminalen; maskinens egne miljøvariabler vinder.
- Ingen `.env` oprettet. Ingen push, intet versionsnummer ændret.

- Runde 2, punkt 6 (tom nøgle i `.env`): `config/settings.py`: `load_env(path)` bruger nu `dotenv_values(path)` og sætter kun en nøgle i miljøet, hvis værdien i filen ikke er tom og nøglen ikke allerede findes på maskinen. En tom nøgle i filen sættes ikke (hverken som tom tekst eller over maskinens værdi), så appens standardværdi gælder. `load_dotenv` er ikke længere brugt. Nøgler, standardværdier, `.env.example` og `CLAUDE.md` er uændrede; deres tekst er stadig rigtig.
- `config/tests.py`: tre nye tests med opdigtede nøgler: tom værdi i filen sættes ikke, mens en ikke-tom værdi i samme fil bruges; tom værdi overskriver ikke maskinens værdi; standardværdien gælder når nøglen er tom i filen. De fire eksisterende tests er uændrede. Punkt 7 (nu "de fire første punkter" plus det nye).
- Commit: `task-0003: behandl en tom nøgle i .env som ikke sat`. Intet pushet, intet versionsnummer ændret.
- Til README (architect): man kan kopiere `.env.example` til `.env` og kun udfylde de nøgler man bruger; tomme nøgler ignoreres.

### Hvad er ikke lavet, og hvorfor
- Hele suiten og `makemigrations --check` kunne ikke køres denne gang (punkt 8, "testsuiten er grøn", er ikke efterprøvet). `.venv` er ændret siden forrige kørsel: `.venv\Lib\site-packages\django\utils\cache.py` er omdøbt til `cache.py.txt`, så `manage.py` fejler med `ModuleNotFoundError: No module named 'django.utils.cache'`. Det ligner en karantæne eller et sikkerhedsværktøj. Jeg har ikke genskabt eller rørt filen. Mit eget arbejde er i stedet efterprøvet med et engangsscript, der kalder `load_env` med en midlertidig fil: tom nøgle sættes ikke, ikke-tom bruges, maskinens værdi bevares. De tre nye tests er ikke kørt.

### Uklart
intet
