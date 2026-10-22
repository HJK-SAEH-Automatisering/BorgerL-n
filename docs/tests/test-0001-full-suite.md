---
nummer: test-0001
titel: Hele testsuiten på grenen task-0002-run-screen-clarity
status: behandlet
rolle: tester
oprettet: 2026-10-22
omfang: Hele suiten, migreringstjek og en læsning af task-0002 mod koden og testene. Ingen browser.
---

# test-0001 — Hele testsuiten på grenen task-0002-run-screen-clarity

## Hvad blev prøvet
- `.venv\Scripts\python.exe manage.py test` (alle apps): 51 tests, alle grønne, ingen sprunget over, ingen advarsler. Kørt tre gange (stabilt).
- `.venv\Scripts\python.exe manage.py makemigrations --check`: "No changes detected". Migreringen `koersel/0002_koersel_uploadet_af_og_tidspunkt` er med og anvendes rent på testdatabasen.
- Gennemlæst grenens kodeændringer (commit `e77cb29` og `fa3efe9`) mod hvert punkt under "Færdig når" i task-0002, og mod de tests der skal dække dem.
- Sammenlignet reglerne i `static/js/undtagelser.js` (hvornår en række er "Klar") med serverens regler (`beregning/engine.py`, `valider`), fordi rulningen bruger skærmkodens regel mens den server-satte markering bruger serverens. De dækker hinanden: JS kender sats, transport, zone og dage; serveren kender desuden "Timer mangler" (kan ikke ske, `minutter` er et positivt heltal uden null) og "Borgeren er ikke afklaret" (kan ikke ske, Undtagelser kan ikke åbnes med uafklarede rækker).
- Et engangsscript uden for repoet (`C:\Users\d1michg\AppData\Local\Temp\claude\C--Users-d1michg-OneDrive---Hj-rring-Kommune-Skrivebord-Michael-Claude-code-BorgerL-n\8d70ff29-f5d6-4dff-8227-624478c48646\scratchpad\probe.py`, kører i en midlertidig testdatabase i hukommelsen) til at prøve afvisning med kun generel fejl (zonetabellen mangler grundtakstens pris). Resultat: siden svarer 200, `data-afvist` er sat, meddelelsen om grundtakst vises, og ingen række er markeret. Det er som besluttet i opgaven. Scriptet efterlader intet i repoet; `git status` er uændret af mig.

## Hvad holdt
- Hele suiten og migreringstjekket er grønne.
- Upload: de fem punkter i "Færdig når" har hver en test i `koersel/tests.py` (sidst uploadet med filnavn, bruger, dato og klokkeslæt; ny upload erstatter alle tre; afvist upload ændrer ingen af felterne; kørsel uden de nye felter viser kun filnavn; slettet bruger giver filnavn og tidspunkt uden navn; uden fil står der "Ingen fil valgt").
- Undtagelser, serversiden: efter afvist beregning bærer formularen `data-afvist` og præcis én række er markeret, den første der mangler. Meddelelsen om hvor mange der mangler og "1 af 3 klar" er uændret. Uden afvisning og efter "Gem kladde" er der ingen markering.
- "Mangler ingen noget, beregnes som i dag": dækket af den eksisterende `test_hele_flowet_beregn_pdf_godkend_eksport`.
- Reglerne for status er uændrede: `engine.py`, `services.valider_koersel` og statusudregningen i JS er ikke rørt i diffen, kun udvidet med markering.
- Ingen nye pakker, skærme, knapper, filtre eller søgning i diffen.
- Skabelonen autoescaper filnavn og brugernavn.

## Hvad blev ikke prøvet
- **Udseende og rulning på Undtagelser er ikke efterprøvet i en browser.** Det gælder at siden faktisk ruller til rækken (både ved lokal afbrydelse og ved indlæsning efter serverafvisning), at rækken er tydelig (gul baggrund, rød kant, i lys og mørk tilstand), at markeringen forsvinder når brugeren retter noget, og at rulningen er rolig når brugeren har bedt om mindre bevægelse. Agenter starter ikke browsere.
- **Skærmkodens logik er ikke kørt.** Der er ingen JS-testopsætning i projektet, og der er ikke bygget nogen. Kun serverens HTML er prøvet.
- Dashboard og Gennemse transport er ikke læst særskilt for at se at de stadig kun viser filnavnet; diffen rører dem ikke, men ingen test fastholder det.
- Auditlogningen ved upload og gem er ikke efterprøvet særskilt; diffen rører ikke linjerne, og eksisterende tests dækker kun at flowet kører.
- MSSQL er ikke prøvet (som før; findes ikke her). Migreringen er kun kørt mod SQLite.
- Hele "Færdig når"-listen er ikke afkrydset af mig; det er `architect`s afgørelse.

## Fund

### F1 — Rulning, markering og fjernelse af markering har ingen automatisk kontrol · alvor: note
**Reproduktion:** Ingen fejl fundet. Opgaven kræver rulning til første række ved "Beregn" (lokalt og efter serverafvisning), og at markeringen fjernes når brugeren retter. Alt det ligger i `static/js/undtagelser.js` (`visFoersteManglende`, `fjernMarkering`). Ingen test kører den kode; testene viser kun at serveren sender `data-afvist` og klassen `mangler`.
**Hvorfor det betyder noget:** Tre af de fem Undtagelser-punkter i task-0002 hviler kun på at developer har læst koden og kørt `node --check` (syntaks). En fejl i rulningen eller i fjernelsen af markeringen ville ikke vise sig i suiten.
**Forslag:** Afgør om en browserprøve ved hånd (mennesket eller `architect`) er nok, eller om projektet skal have en JS-testopsætning. Det sidste er en ny afhængighed og hører i så fald i en egen opgave.

### F2 — Serverens og skærmkodens "første manglende række" er to uafhængige udregninger uden fælles kontrol · alvor: note
**Reproduktion:** Efter afvist beregning markerer serveren første række med `fejl` (`foerste_mangler` i `koersel/views.py`). Ved indlæsning kalder JS `visFoersteManglende()`, som først fjerner alle markeringer og derefter markerer første række hvis statusmærke ikke er `ok` ud fra skærmkodens egne regler. I dag giver de samme række (se "Hvad blev prøvet"). Ingen test fastholder at reglerne forbliver ens.
**Hvorfor det betyder noget:** Ændres reglerne i `engine.valider` uden at JS følger med (eller omvendt), kan serveren markere én række og skærmkoden flytte markeringen til en anden, eller fjerne den helt hvis JS ser alle som klare. Det er en tilstand der først bliver en fejl ved en senere regelændring, ikke i dag.
**Forslag:** Enten en note i opgave- eller kodetekst om at de to skal holdes ens, eller en test der kører en række tilfælde gennem serverens regel og sammenligner med skærmkodens. Alternativt at JS ved indlæsning efter afvisning bruger rækken serveren allerede har markeret, i stedet for at udregne den igen (developer har selv nævnt dobbeltheden i sine noter).

### F3 — Afvisning med kun generelle fejl er ikke dækket af en test · alvor: note
**Reproduktion:** Slet prisen for 2 zoner i zonetabellen og tryk "Beregn". Faktisk (prøvet med engangsscriptet): 200, `data-afvist="1"` sat, meddelelse om grundtakst vist, ingen række markeret, ingen fejl. Det er det opgaven har besluttet ("ingen særlig behandling"). Der er ingen test i `koersel/tests.py` der fastholder det.
**Hvorfor det betyder noget:** Adfærden er beslutning, men kan kun brydes ubemærket. Lav konsekvens.
**Forslag:** En kort test for netop dette tilfælde, hvis `architect` vil fastholde beslutningen.

### F4 — "Dashboard og Gennemse viser stadig kun filnavnet" er ikke fastholdt af en test · alvor: note
**Reproduktion:** Ingen fejl. Opgaven har det som afgrænsning; ingen test hævder at de to skærme ikke viser bruger og tidspunkt.
**Hvorfor det betyder noget:** En senere ændring af de delte skabeloner kunne utilsigtet vise tidspunkt og brugernavn andre steder uden at en test reagerede. Lav konsekvens.
**Forslag:** Kun hvis det ønskes fastholdt: en test på de to skærme. Ellers ingen handling.

## Uklart
- Skal en browserprøve af udseende og rulning udføres af mennesket før grenen lukkes? Jeg har ikke afgjort det og kan ikke selv gøre det.
- Intet andet.

## Afledte numre
intet — alle fire fund er afvist; se beslutningsloggen.
