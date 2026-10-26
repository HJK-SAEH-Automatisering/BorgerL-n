---
nummer: task-0007
titel: Skift ordet borger til medarbejder, og navnet BorgerLøn til MedarbejderLøn
kilde: interview
status: i-gang
oprettet: 2026-10-26
---

# task-0007 — Skift ordet borger til medarbejder, og navnet BorgerLøn til MedarbejderLøn

## Hvad og hvorfor
Mennesket vil ikke, at appen siger "borger". Personerne skal hedde "medarbejder" overalt, hvor nogen læser det, fx "Medarbejderregister" i stedet for "Borgerregister". Appens synlige navn skifter fra "BorgerLøn" til "MedarbejderLøn". Opgaven ændrer kun det, der kan læses. Navne i koden, tabeller, adresser i browseren, mappen og repoet på GitHub bliver, som de er.

## Færdig når
Skærmene:

- [ ] Ingen skærm viser længere ordet "borger" i nogen form, hverken i topbjælke, menuer, overskrifter, knapper, tabeloverskrifter, meddelelser, fejl, hjælpetekster, formularfelter, tomme tilstande eller advarsler. "Borgere" er blevet til "Medarbejdere", "borgerens" til "medarbejderens", og "Borgerregister" til "Medarbejderregister". Bøjninger og sammensatte ord følger med.
- [ ] Appens synlige navn er "MedarbejderLøn" i topbjælken, i sidernes titler og på loginsiden.
- [ ] Administrationssiden viser medarbejder og medarbejdere i stedet for borger og borgere, også i overskrifter og feltnavne.

Rapporter og eksport:

- [ ] Nye PDF-rapporter og nyt lønudtræk (CSV) bruger ordet "medarbejder" og navnet "MedarbejderLøn", hvor ordet i dag står.
- [ ] Allerede gemte PDF-rapporter er uændrede, og kontrollen af en gemt rapport virker stadig for dem.

Dokumenter:

- [ ] `README.md`, `CLAUDE.md` og `docs/losningsforslag.md` bruger "medarbejder" og "MedarbejderLøn". `CLAUDE.md` og `README.md` nævner, at mappen og repoet stadig hedder BorgerLøn.
- [ ] Skitserne under `docs/mockups/`, beslutningsloggen, de afsluttede opgaver og testrapporterne er uændrede. De er historik.

Uændret:

- [ ] Gemte data virker uændret. Eksisterende kørsler, medarbejdere og rapporter kan åbnes som før.
- [ ] Alle adresser i browseren er uændrede.
- [ ] Beregningen giver de samme beløb som før.

Fælles:

- [ ] Tests, der kontrollerer tekster, er rettet til de nye ord. Der er en test, der viser, at ingen af skærmene indeholder "borger" i det synlige indhold.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- **Skel mellem tekst og navne i koden.** Ordet står mange steder i koden som navne på variabler, klasser og funktioner. Dem rører vi ikke. Kun tekst, brugeren kan læse: skabeloner, meddelelser og fejl i visningerne og formularerne, hjælpetekster og feltnavne, visningsnavne i administrationen (`verbose_name`), advarsler fra beregningen, rapportens og eksportens tekster, og skærmkodens tekster.
- **Navne og adresser bliver.** Modellernes navne, tabellerne, adressernes sti og navne, og eksisterende migreringer ændres ikke. Ændrede visningsnavne giver en ny migrering uden betydning for data; den laves med `makemigrations`.
- **PDF-rapporten.** Ordene ændres i `beregning/pdf.py`. Står der et layoutnummer, som skal øges, når rapportens tekst ændres, øges det, og det skrives i noterne. Allerede gemte PDF-filer ændres aldrig.
- **Grammatik.** Ordene følger dansk: "en medarbejder", "medarbejderen", "medarbejdere", "medarbejdernes", "medarbejderens", "medarbejderregistret".
- **Navnet.** "BorgerLøn" skifter til "MedarbejderLøn" i det synlige. Mappen, repoet, `.claude/launch.json` og kodens navne bliver.
- **Søgning til sidst.** Udvikleren søger efter ordet i skabeloner, tekster i koden og dokumenterne og skriver i sine noter, hvad der er tilbage, og hvorfor det er et navn i koden.

## Hvad vi ikke rører
- Navne i koden, modellernes navne, tabeller og eksisterende migreringer.
- Adresser i browseren.
- Beregningsmotorens regler og beløb.
- Mappen og repoet på GitHub.
- Skitserne, beslutningsloggen, afsluttede opgaver og testrapporter.
- Demodataenes fiktive navne.

## Afhænger af
task-0006 — begge ændrer Godkend-skærmen og de tests, der kontrollerer dens tekster. Der bygges kun på én opgave ad gangen, og denne sendes først af sted, når task-0006 er afsluttet.

## Beslutninger
- BESLUTTET: Kun synlig tekst ændres — navne i koden, tabeller og adresser bliver. En omdøbning af dem er en stor og risikabel ændring uden gevinst for brugerne. Afvist: omdøbning af modeller, tabeller og adresser.
- BESLUTTET: Det synlige navn skifter til "MedarbejderLøn" — mennesket valgte det, fordi navnet indeholder ordet. Mappen og repoet bliver. Afvist: at omdøbe repoet nu.
- BESLUTTET: Gemte PDF-rapporter ændres ikke — den gemte PDF er selve beviset på en beregning.
- BESLUTTET: `README.md`, `CLAUDE.md` og `docs/losningsforslag.md` rettes, men skitser, beslutningslog, afsluttede opgaver og testrapporter gør ikke — de er historik.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
Gren: `task-0007-employee-wording`. Commits på grenen, ingen push, intet versionsnummer ændret. Ingen nye kommandoer eller indstillinger.

Skærmene:
- `templates/base.html`: topbjælken og sidetitlen hedder "MedarbejderLøn", menupunktet "Borgere" hedder "Medarbejdere". Loginsiden arver titlen fra `base.html`.
- `templates/register/borger_liste.html`, `templates/register/borger_form.html`: "Medarbejderregister", "Opret medarbejder", "Ret medarbejder", "Søg medarbejder", "Ingen medarbejdere fundet", "Medarbejderen knyttes til rækken ...".
- `templates/koersel/gennemse.html`, `godkend.html`, `undtagelser.html`, `upload.html`: overskrifter, hjælpetekster, kolonnen "Medarbejder", "Vælg medarbejder i registret", "Opret ny medarbejder", "Beregning pr. medarbejder", "Eksport er låst, til alle medarbejdere er godkendt", `aria-label`.
- `static/js/undtagelser.js`: "medarbejder/medarbejdere mangler oplysninger, før du kan beregne".
- `koersel/views.py`, `koersel/services.py`, `register/views.py`: meddelelser og fejl ("Vælg en medarbejder i listen.", "Medarbejderen er ikke afklaret.", "Der er ingen medarbejdere at beregne ...", "N medarbejder(e) godkendt.", m.fl.). Nye linjer i auditloggen skrives også med det nye ord ("Oprettede medarbejder", "Ændrede medarbejder", "Ændrede medarbejder fra gennemsyn", "... i admin", og antallet i "Kørte beregning").
- Administrationen: `register/models.py` får `verbose_name = "medarbejder"` / `verbose_name_plural = "medarbejdere"`. `koersel/models.py`: feltet `Linje.borger` får `verbose_name="medarbejder"`, og hjælpeteksten på `kandidater` er rettet. Administrationen har ingen egne overskrifter i `config/urls.py` eller `admin.py`, så der var ikke mere at rette.
- Migreringer: `register/migrations/0002_alter_borger_options.py` og `koersel/migrations/0004_alter_linje_borger_alter_linje_kandidater.py`, lavet med `makemigrations`. Kun visningsnavne og hjælpetekst; ingen datakopiering, ingen skemaændring. De er endnu ikke kørt mod den lokale `db.sqlite3` (kør `manage.py migrate`; den kørende server ser ikke forskel).
- `register/management/commands/seed_demo.py`: hjælpeteksten. Kommandoens øvrige udskrifter indeholder ikke ordet.

Rapporter og eksport:
- `beregning/engine.py`: "Sats pr. time mangler på medarbejderen.", trinnet "Medarbejderens egenbetaling for transport" og dets forklaring, "medarbejderens egenbetaling trækkes i lønnen". Beløb og regler uændrede.
- `beregning/pdf.py`: "Antal medarbejdere", "for hver medarbejder", kilden "Medarbejderregistret", forfatter i PDF-metadata "MedarbejderLøn". **`LAYOUT_VERSION` øget fra 1 til 2**, fordi rapportens tekst er ændret.
- CSV-udtrækket (`koersel/services.py`, `lav_csv`): indeholder slet ikke ordet i dag (kolonnerne er Tj.nr., Navn, Afdeling, Timer, Løn før skat, Træk, Udbetaling), så der er intet at rette. Testen kontrollerer det.
- Gemte rapporter: ingen PDF-fil, snapshot eller databaserække er rørt. Prøvet med `manage.py verificer_rapport 2026-10-001` og `2026-10-007` på den lokale database: begge melder "den gemte PDF er uændret", og at den genskabte PDF afviger fordi layoutet er ændret (gemt layout `?` hhv. 1, nu 2). Exit 0, som designet.

Dokumenter:
- `README.md`: "MedarbejderLøn", "medarbejdere", og en linje om at mappen og repoet stadig hedder BorgerLøn. Sætningen "beregningen borger for borger" er skrevet som "beregningen for én medarbejder ad gangen", fordi "medarbejder for medarbejder" blandede brugeren (en administrativ medarbejder) og de personer, der får løn.
- `CLAUDE.md`: samme rettelser, et afsnit "Navnet" om at mappen, repoet og kodens navne (`Borger`, tabeller, `borger_*.html`, adressenavne, `/borgere/`, feltnavnet `borger`) bliver, og tabelrækken for `register/`.
- `docs/losningsforslag.md`: alle forekomster rettet, undtagen `BorgerLookupProvider` (navn på en grænseflade i koden).
- Rørt ikke: `docs/mockups/`, `docs/decisions/log.md`, `docs/tasks/` (ud over disse noter), `docs/tests/`, `docs/BOARD.md`, `.claude/launch.json`.

Tests:
- Tekstkontroller rettet i `koersel/tests.py`, `register/tests.py`, `beregning/test_engine.py`.
- Ny test `FlowTests.test_ingen_skaerm_indeholder_ordet_borger` (`koersel/tests.py`): henter login (uden login), forside, medarbejderliste (også tom), ny og ret medarbejder, upload, gennemse (med uafklaret række), ny medarbejder fra række, undtagelser (afvist og uafvist), godkend, beregningsgrundlag og administrationens sider for medarbejdere, og kontrollerer, at der ikke står "borger" (uanset store og små bogstaver) i tekst og i `aria-label`, `placeholder`, `title` og `alt`. Den læser også de meddelelser, der kommer efter handlinger, snapshot og CSV, og tjekker at `undtagelser.js` ikke indeholder ordet. Fiktive data ("Person 1" osv.). Jeg har set testen fejle, når en `aria-label` med ordet sættes tilbage.
- Ny test `FlowTests.test_rapporten_bruger_ordet_medarbejder`: nyt snapshot har `rapport_layout == 2`, og PDF-teksten (uden komprimering) indeholder "antal medarbejdere" og ikke "borger".

Kørt:
- `.venv\Scripts\python.exe manage.py test`: "Ran 79 tests ... OK" (79 tests, alle grønne).
- `.venv\Scripts\python.exe manage.py makemigrations --check`: "No changes detected", exit 0.
- Udseendet er ikke efterprøvet visuelt (ingen browser startet). Kun HTML og tekst er kontrolleret.

Søgning til sidst (hvad der stadig indeholder "borger", alt sammen navne i koden eller beskrivelser af dem):
- Skabeloner: kun `{% url 'borger_liste/borger_ny/borger_ret' %}`, `l.borger`, `borger.navn/.pk/.cpr`, `borgere` (kontekstvariabel), `name="borger"` (formularfelt) og filnavnene `borger_liste.html`/`borger_form.html`. Intet af det vises.
- Kode: modellen `Borger`, `BorgerForm`, `BorgerAdmin`, feltet/relationen `borger` og `borger__afdeling`, `saet_borger`, variablerne `borger`/`alle_borgere`/`borgere_pr_navn`/`antal_pr_borger`, visningerne `borger_liste/ny/ret`, adressenavnene og stien `borgere/` i `config/urls.py`, tabellen `register_borger`, eksisterende migreringer, `stamdata/migrations/0002` (seed), `config/tests.py` (nøglerne `BORGERLON_TEST_A/B`) og `tempfile`-præfikset `borgerlon-test-`.
- Øvrigt: `.claude/launch.json` (`borgerlon`), kommentaren i `.gitignore`, `BorgerLookupProvider` i `docs/losningsforslag.md`, og de to omtaler af mappen/repoet i `README.md` og `CLAUDE.md`.

### Hvad er ikke lavet, og hvorfor
- Gamle gemte kørsler viser stadig de gamle ord. Advarsler og trin i et gemt snapshot (fx "Sats pr. time mangler på borgeren.", "Borgerens egenbetaling for transport") læses fra snapshotten, så Godkend-skærmen og beregningsgrundlaget for kørsler beregnet før denne opgave viser dem uændret. Det følger af, at snapshots er uforanderlige; kun nye beregninger får de nye ord. Ikke en fejl, men "ingen skærm viser borger" gælder derfor kun nye beregninger.
- Auditlog-siden i administrationen viser stadig "Borger" i kolonnen og filteret "objekt_type" (klassenavnet, gemt som data), og de gamle linjer i `handling` hedder fortsat "Oprettede borger" osv. Nye handlinger får det nye ord, så filteret viser nu begge ord. Jeg har ikke ændret gemte data eller logfunktionen, der skriver klassenavnet.
- Ingen browser, så udseendet er ikke efterprøvet.
- `manage.py migrate` er ikke kørt mod den lokale database (migreringerne er rene visningsændringer).

### Uklart
- Skal auditloggens objekttype ("Borger") vises som "Medarbejder" i administrationen? Det kræver en visningsmetode og et eget filter, ikke en dataændring; jeg gjorde det ikke, fordi det ligger uden for det opgaven nævner. Kriteriet "administrationssiden viser medarbejder i stedet for borger" er ellers opfyldt for de sider, testen dækker (forside, medarbejderliste, ny og ret).
- Ordet "medarbejder" betyder nu både brugeren ("Kun administrative medarbejdere har adgang" på loginsiden, "administrative medarbejdere" i `docs/losningsforslag.md`) og de personer, der får løn. Jeg har ikke ændret loginsidens sætning, fordi den ikke indeholdt "borger". Ønsker mennesket en tydeligere forskel (fx "administrative brugere"), er det en ny opgave.
- Fund uden for opgaven (ikke rettet): på Gennemse-skærmen er der en tom valgmulighed i listen "Vælg medarbejder i registret" (`value=""`). Trykker man på knappen til afklaring uden at vælge, kalder `koersel/views.py` (omkring linje 95) `Borger.objects.filter(pk="")`, og det giver en serverfejl (`ValueError: Field 'id' expected a number but got ''`) frem for beskeden "Vælg en medarbejder i listen.". Min test bruger derfor et ukendt nummer for at nå beskeden. Det samme gælder før denne opgave.
