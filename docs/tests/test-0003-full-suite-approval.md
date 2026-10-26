---
nummer: test-0003
titel: Fuld suite og rester efter task-0005 (simplificeret Godkend-skærm)
status: behandlet
rolle: tester
oprettet: 2026-10-26
omfang: hele testsuiten, makemigrations --check, søgning efter rester af fjernede dele, den nye test for Godkend-skærmen, på grenen task-0005-simplify-approval
---

# test-0003 — Fuld suite og rester efter task-0005

## Hvad blev prøvet
- `.venv\Scripts\python.exe manage.py test` (alle apps, 73 tests) på grenen `task-0005-simplify-approval`.
- `.venv\Scripts\python.exe manage.py makemigrations --check`.
- Søgning (uden hensyn til store/små bogstaver) i `templates/`, `static/`, `koersel/`, `register/`, `beregning/`, `config/`, `stamdata/` og `audit/` efter `tiles`, `tile`, `totaler`, `godkendt_antal`.
- Læsning af grenens diff mod `main` for skabelon, visning og CSS.
- Den nye test `test_godkend_skaermen_har_ikke_rapportlinje_forklaring_eller_totaler`: læst, og kørt som en del af suiten.
- Et engangsscript uden for repoet (`C:\Users\d1michg\AppData\Local\Temp\claude\C--Users-d1michg-OneDrive---Hj-rring-Kommune-Skrivebord-Michael-Claude-code-BorgerL-n\8d70ff29-f5d6-4dff-8227-624478c48646\scratchpad\probe\probe_godkend.py`). Det gentager den nye tests forløb (før og efter "Godkend alle") og tjekker også at PDF-rapporten kan hentes. Eneste forskel er at påstanden om "Løn efter skat" er udeladt (se F1). Scriptet er ikke en del af projektet.
- `.venv` virkede uden spærring eller karantæne. Intet blev genskabt eller installeret.

## Hvad holdt
- Suiten: 73 tests, 72 grønne, 1 rød (se F1). Systemtjekket meldte ingen problemer.
- `makemigrations --check`: "No changes detected".
- Rester: ingen henvisninger til `tiles`, `tile` eller `godkendt_antal` i skabeloner, CSS eller kode udover den nye test. `totaler` findes kun i `beregning/pdf.py` og `koersel/services.py` (de gemte data og rapporten, som opgaven ikke rører) og i den nye test. Ingen skabelon eller visning henviser til de fjernede kontekstværdier.
- Det kørte svar fra Godkend-skærmen (test-klient) indeholder ikke `class="tiles"`, `class="tile"`, "Gennemgå, hvordan beløbet er beregnet", "x af y godkendt", "Rapport <id> ·", "Træk (lønart 991)" eller "Udbetaling (lønart 991)", hverken før eller efter "Godkend alle" (engangsscriptet).
- Det der skal blive, står i svaret begge steder: overskriften "Godkend beregning · <måned>", knappen "Åbn PDF-rapport <nummer>", "Beregning pr. borger", "Tidligere beregninger for måneden", "Tilbage til undtagelser".
- Før godkendelse: "Godkend alle" og "Eksport er låst, til alle borgere er godkendt." står der. Efter: "Genåbn til rettelser" og eksportknappen "Eksportér lønudtræk (CSV)" står der, og låsteksten er væk.
- PDF-rapporten kan hentes (status 200) fra den rute knappen peger på.
- Den nye test kontrollerer både før og efter "Godkend alle": hjælpefunktionen `tjek_fjernet` kaldes begge steder, og tilstandsspecifikke påstande står efter hver af de to kald (låst/Godkend alle før, Genåbn/eksportknap/ingen lås efter). Opbygningen er rigtig; den fejler kun på én påstand (F1).
- Grenens diff rører kun skabelonen, visningen, CSS'en, den nye test og papirsporet. Ingen anden skærm eller motoren er ændret.

## Hvad blev ikke prøvet
- Udseende. Der er ikke startet nogen browser, så layout, afstande og om skærmen ser rigtig ud efter fjernelsen af rækken og CSS-reglerne, er ikke efterprøvet. Det hører til `architect` eller mennesket.
- Om knapperne og "Genåbn" virker ved klik i en browser. Kun HTTP-kald via Djangos testklient og påstande om HTML'en.
- Dokumentation og README (om de nævner totalerne på skærmen). Det er `reviewer`s, ikke adfærd.
- MSSQL. Suiten kører mod SQLite, som i projektets øvrige test.

## Fund

### F1 — Den nye test fejler på en påstand der rammer en del der skal blive · alvor: middel
**Reproduktion:** Kør `.venv\Scripts\python.exe manage.py test koersel.tests.FlowTests.test_godkend_skaermen_har_ikke_rapportlinje_forklaring_eller_totaler`.
Forventet: grøn. Faktisk: `AssertionError: 2 != 0 : 'Løn efter skat' unexpectedly found in the following response` ved `koersel/tests.py` linje 371 (`self.assertNotContains(svar, "Løn efter skat")`), kaldt fra linje 382 (første gennemløb, før "Godkend alle").
Årsag: "Løn efter skat" står to gange i svaret som trin 4 i "Se beregningsgrundlag" for hver borger. Det hører til "Beregning pr. borger", som opgaven siger skal være uændret. Skærmen er altså ikke forkert; påstanden er for bred og giver falsk alarm. Det er den eneste røde test i suiten, så "Testsuiten er grøn" i opgavens "Færdig når" er ikke opfyldt, som grenen står.
Engangsscriptet (samme forløb uden denne ene påstand) er grønt, både før og efter "Godkend alle". Det viser at resten af påstandene holder mod det kørte svar.
**Hvorfor det betyder noget:** Opgavens kriterium "Testsuiten er grøn" er ikke opfyldt, og en test der fejler på det rigtige indhold vil enten blive overset eller slettet. Så mister grenen den kontrol der skal vise at totalerne er væk. Samme risiko gælder de andre tekstmærker: "Løn før skat" står også i listen pr. borger og kan ikke bruges som mærke.
**Forslag:** En opgave til `developer`: lad påstanden pege på det der kun fandtes i totalrækken, fx hele flisen (`<div class="l">Løn efter skat</div>`) eller afgrænse til området før "Beregning pr. borger". Ret ikke de to klasse-påstande, de virker.

### F2 — De fjernede totaler og "x af y godkendt" er kun dækket af negative tekstmærker · alvor: note
**Reproduktion:** Læs `koersel/tests.py` linje 361–373. Rækken er påvist væk via klassenavne (`tiles`, `tile`) og to labeltekster. Totalen "Borgere" og "Løn før skat" er ikke påvist, fordi teksterne også står andre steder på skærmen.
**Hvorfor det betyder noget:** Bliver rækken bygget igen med andre klassenavne, ser testen det ikke. Konsekvensen er lille (en skærm der er mere fyldt end besluttet), og klassenavnene var det der faktisk stod i skabelonen.
**Forslag:** Ingen handling nødvendig udover F1. Nævnes kun fordi der ikke er en positiv kontrol af skærmens samlede indhold.

## Uklart
- Om `README.md` eller `docs/losningsforslag.md` beskriver Godkend-skærmen med totalerne. Det er ikke undersøgt her (prosa); det er en sag for `reviewer`.
- Jeg antog at "Løn efter skat" i beregningsgrundlaget er tilsigtet og skal blive, fordi opgaven siger at "Beregning pr. borger" er uændret med beregningsgrundlag.

## Afledte numre
intet nyt nummer — fund 1 er rettet inden for task-0005; fund 2 er afvist. Se beslutningsloggen.
