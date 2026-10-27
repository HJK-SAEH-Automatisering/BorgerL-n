---
nummer: test-0004
titel: Sammenhæng på tværs af task-0006 til task-0014
status: behandlet
rolle: tester
oprettet: 2026-10-27
omfang: hele månedsflowet, Godkend-skærmens tilstande, beregningsgrundlaget, ordskiftet, versionsnumre på stilark og skærmkode, auditlog i administrationen, PDF og kontrol af rapporter, randtilfælde på tværs, og reparationsscriptet (kun tjek-tilstand)
---

# test-0004 — Sammenhæng på tværs af task-0006 til task-0014

## Spærring mødt under prøven (læs først)
Filen `django/utils/cache.py` i projektets `.venv` er under min prøve blevet erstattet af en karantænefil. Der ligger nu kun `cache.py.txt` (tidsstempel i dag kl. 10:30:09, 150 bytes, begynder med en byte-orden-markør og derefter sætningen om at filen er sat i karantæne på grund af Web Reputation, og at man skal kontakte sin Cloud App Security-administrator). Alle mine kørsler med `manage.py` (suite, `verificer_rapport`, midlertidig server) lykkedes, før jeg opdagede det, så karantænen er kommet bagefter. Jeg opdagede den ved et sidste kald af reparationsscriptet i `--tjek`-tilstand, som melder den korrekt (se "Hvad holdt").

Jeg har ikke kørt scriptet i gendan-tilstand, ikke genskabt filen og ikke rørt noget andet i `.venv`. Konsekvens for mennesket: den kørende server på port 8000 har Django i hukommelsen og kan fortsætte, men en ny opstart, `manage.py` og testkørsel vil fejle med "No module named 'django.utils.cache'", til reparationsscriptet er kørt (eller `.venv` er bygget forfra). Det er en beslutning for mennesket og `architect`.

## Hvad blev prøvet
Alt nedenfor er kørt med almindelige HTTP-kald (Python, standardbiblioteket) mod min egen udviklingsserver på port 8011 med `--noreload`, en midlertidig SQLite-fil og en midlertidig MEDIA_ROOT i systemets temp-mappe uden for projektet og OneDrive. Projektets `db.sqlite3` (uændret tidsstempel), `media/` og `.env` er ikke læst eller rørt. Ingen browser er startet. Serveren er stoppet, den midlertidige mappe og mine engangsscripts (uden for repoet) er slettet, og jeg har kontrolleret, at kun menneskets server på 8000 kører. `eksempel/punchly-eksempel.xlsx` (ignoreret af git) blev overskrevet af `seed_demo`; jeg har lagt den oprindelige kopi tilbage.

Månedsflowet (task-0001 til 0005 som baggrund):
- Opret kørsel (to måneder: 2026-10, 2026-09, og en tredje 2026-08), upload af eksempelfilen, gennemse, undtagelser, beregn, godkend, eksport, PDF.
- Upload: filer med "Antal arbejdsdage" og "Antal dage", uden kolonnen, med tomme celler, og med ugyldige værdier (0, 32, "abc", -3, 3,5). Ugyldige værdier afviser hele filen med række og værdi, og kørslens rækker er uændrede. Filtype og beskadiget fil afvises med besked. Samme navn flere gange (også med anden store/små og ekstra mellemrum): rækkerne vises hver for sig med markering, og beregningen giver advarslen om mulig dobbeltansættelse.
- Gennemse: række uden match, række med flere mulige (afklaring viser kun kandidaterne), afklar med valg, afklar uden valg (tom værdi, helt manglende felt, "abc", ukendt nummer: besked "Vælg en medarbejder i listen.", intet ændret, ingen serverfejl), afklar mod en medarbejder, der allerede er matchet i en anden række, "Opret ny medarbejder" fra en række, gem med ugyldig afstand.
- Undtagelser: Beregn med manglende zone (afvist, første manglende række markeres, besked), individuel beregning slået til uden dage (feltet står forudfyldt med dagene fra filen efter gem), dage 0, 99, "abc", individuel på taxa (ryddes), Beregn efter rettelse.
- Godkend-skærmen i alle tilstande: ingen godkendt, én godkendt, alle godkendt, efter Genåbn (både fra delvist og helt godkendt), gentagne Genåbn, Godkend alle igen. For hver tilstand: knappernes rækkefølge, om de er knapper eller links, om de er deaktiverede og har forklaringen "Kan først bruges, når alle medarbejdere er godkendt.", om "Godkend alle" er grøn og deaktiveret, antal grønne rækkeknapper, rækkernes opbygning (samme to knapper i alle 13 rækker), titlen på den grønne knap ("Godkendt af <bruger> <tid>"), flash-beskeder, kørslens status i databasen, antal godkendte resultater i databasen, og auditlog-linjer.
- Eksport og PDF: direkte adresse til eksport med nogle godkendt (afvises, ingen fil) og efter Genåbn; eksport med alle godkendt (CSV med de forventede kolonner, uden CPR); PDF åbner.
- Ny Beregn efter godkendelser (delvist godkendt): ny beregning 002 står uden godkendelser, gamle godkendelser hører til 001 og tæller ikke, kørslens status bliver "beregnet". Historikken viser 002 som gældende. Låsning: undtagelser, gennemse og upload sender en godkendt kørsel til Godkend med besked, og en POST til Beregn mens den er godkendt gør intet.
- Upload af en ny fil efter Genåbn (se F1).
- To kørsler side om side: godkendelser i den ene rører ikke den anden. Et resultatnummer fra den ene brugt via den anden kørsels adresse giver 404 på beregningsgrundlaget og "Intet at godkende" ved godkendelse.
- Grundlagssiden: kræver login (omdirigerer), 404 for ukendt nummer, tekstnummer, forkert kørsel, og for et resultat fra en tidligere beregning (gammelt nummer). Indholdet viser navn, Tj.nr., afdeling, timer, transport og trin-tabellen; uden trinsøjle, uden godkendelsesknap, uden CPR og uden adresse.
- Ordet "borger" og navnet "BorgerLøn": 20 sider hentet (login, forside, medarbejderliste med og uden inaktive, ny/ret medarbejder, upload, gennemse med og uden rettetilstand, undtagelser, godkend, grundlag, og administrationens forside, medarbejdere, ret/ny medarbejder, auditlog, kørsler, beregningskørsler, afdelinger, brugere). Søgt i synlig tekst og i `aria-label`, `placeholder`, `title` og `alt`. Ingen fund på nye kørsler. CSV-udtrækket og en ny PDF (genskabt uden komprimering ud fra snapshotten) indeholder "medarbejder" og ikke "borger" eller "BorgerLøn"; PDF-metadata har "MedarbejderLøn". PDF'en indeholder hverken CPR eller adresse.
- Gamle snapshots: jeg ændrede i min midlertidige database snapshottet på én beregning, så det mangler layoutnummeret og har gamle ord i en advarsel og et trin. Godkend-skærmen og grundlagssiden åbner uden fejl og viser de gamle ord ("borgeren", "Borgerens"). Det er det, task-0007 beskriver.
- Stilark og skærmkode: alle ni forskellige sider i appen (også login uden at være logget ind) henter `app.css?v=<tal>`, og Undtagelser henter `undtagelser.js?v=<tal>`. Tallet er filens ændringstidspunkt i nanosekunder (sammenholdt med filsystemet), og begge adresser leverer filen (200, rigtig indholdstype).
- Administration: auditloggen viser objekttypen "Medarbejder" for gemte poster med typen Borger, og de øvrige typer som de er. Filteret viser "Medarbejder" og filtrerer på den gemte værdi (`objekt_type=Borger` giver kun de poster; `objekt_type=Medarbejder` giver ingen, `xyz` giver ingen uden fejl). Sortering på kolonnen og søgning virker. Handlingsfilteret viser kun de nye tekster i min database ("Genåbnede kørsel").
- Login og adgang: alle ruter, også grundlag, eksport, PDF, `borgere/` og administration, sender til login uden session. POST uden CSRF-nøgle giver 403. Ukendt kørsel og ukendt rapport giver 404.
- Auditlog-tekster efter flowet: "Genåbnede kørsel" med "<måned>, fjernede godkendelser: N" (1 og 13 set), "Godkendte beregning" med "N linjer, rapport …", og ingen linje, når Genåbn ikke har nogen virkning.
- Kontrol af rapporter: `verificer_rapport` for tre nye rapporter (uændret, og genskabt identisk), for en rapport med manipuleret snapshot uden layoutnummer (uændret gemt PDF, genskabt afviger, forklares med layout "?" mod 2, returkode 0), og for et ukendt nummer (CommandError, returkode 1).
- Suite og migreringer: `manage.py test` gav "Ran 123 tests ... OK", `makemigrations --check` gav "No changes detected", og `python -m unittest scripts.test_reparer_miljo` gav 23 grønne.
- Reparationsscriptet: læst mod task-0014. Kørt i `--tjek` mod den rigtige `.venv` (først "i orden", returkode 0; til sidst, efter karantænen, melder det den, returkode 1, fra en anden arbejdsmappe end projektroden). Derudover kørt mod en opdigtet `.venv` i en midlertidig mappe med indsprøjtet pip-kald og indsprøjtet import (se "Hvad holdt").
- Læsning på tværs: `kan_eksportere`, `alle_godkendt`, kørslens status og rækkernes `godkendt` i `godkend.html`, `views.py` og `services.py`; om en senere opgave har overstyret en tidligere.

## Hvad holdt
- Hele månedsflowet fra oprettelse til eksport og PDF hænger sammen, og beløbene i CSV passer til skærmen. Auditlog og status følger hver handling.
- Knapperne øverst står i rækkefølgen Godkend alle, Genåbn til rettelser, Eksportér lønudtræk (CSV), Åbn PDF-rapport (nr.) i alle fire tilstande. Eksport og PDF er deaktiverede knapper uden adresse før alle er godkendt (også med én godkendt), og links efter. "Godkend alle" er aktiv, indtil alle er godkendt, og derefter en grøn, deaktiveret knap med samme tekst. Mærket "Godkendt" øverst og teksten "Eksport er låst…" er væk. "Åbn PDF" i listen over tidligere beregninger er uændret.
- Rækkerne har samme opbygning i alle 13 rækker i alle tilstande: knappen Godkend (aktiv, eller grøn og deaktiveret med titlen "Godkendt af … tid") og linket Beregningsgrundlag. Ingen mærker "Afventer" eller "Godkendt", og ingen statuskolonne.
- Genåbn fjerner alle godkendelser (1 af 13, og 13 af 13), efterlader status "beregnet", alle rækker som ikke godkendt, "Godkend alle" aktiv, eksport og PDF låst, og man bliver på Godkend. Eksportadressen afviser uden alle godkendt, også direkte. Gentagne tryk er uskadelige: andet tryk ændrer og logger intet. Auditloggen viser antallet.
- Kørslens status, de grønne rækker, "Godkend alle" øverst og `kan_eksportere` var enige i alle tilstande, jeg kunne nå via skærmene (ingen godkendt, nogle, alle, efter Genåbn, efter ny Beregn). En uenighed kan kun opstå ved ændring direkte i databasen (administrationens kørselssider er skrivebeskyttede).
- Beregningsgrundlaget: login, 404'erne, ingen CPR og adresse, ingen trinsøjle. Siden følger den gældende beregning og giver 404 for en tidligere.
- Ordskiftet på de 20 sider og i nye PDF'er og CSV. Auditlogkolonnen og filteret i administrationen.
- Versionsnumre på stilark og skærmkode på alle sider.
- Reparationsscriptet: sundt miljø giver "i orden" uden ændring (returkode 0). Karantænefilen i den rigtige `.venv` blev fundet af `--tjek` (Django 6.1.2, `django/utils/cache.py.txt`, returkode 1, "intet er ændret"), så den faktiske karantæneteksten med byte-orden-markør matcher scriptets tekst. Mod den opdigtede `.venv`: gendan kalder pip præcis én gang pr. pakke med `--force-reinstall --no-deps Django==6.1.2`; to ramte filer i samme pakke giver ét kald; en `.py.txt` med den originale `.py` ved siden af ignoreres; ukendt pakke giver returkode 2 og ingen kald; en fil med en helt anden ordlyd eller andre endelser (`.pyd.txt`, `.txt`) findes ikke og scriptet melder "i orden". Scriptet skriver, sletter og omdøber ingen filer selv.

## Hvad blev ikke prøvet
- Udseende: farver, afstande, bredder, om knapperne står ved siden af hinanden og ikke går ud over det hvide område, om rækkerne flytter sig, mørk tilstand, hover. Ikke efterprøvet. Det hører til `architect` eller mennesket.
- Skærmkode i en browser: forudfyldning af dage ved klik på individuel beregning, rulning til første manglende række, status og tæller. Jeg har kun set, hvad serveren sender; `static/js/undtagelser.js` er læst, men ikke kørt.
- Selve gendannelsen mod et rigtigt pakkeregister (kræver netværk og ændrer `.venv`). Kørsel af scriptet i gendan-tilstand mod den rigtige `.venv`: bevidst ikke gjort, og efter at karantænen kom, er det spærret af reglen om ikke at gendanne selv.
- At pip selv sættes i karantæne: ikke muligt at prøve uden at røre den rigtige `.venv`.
- MSSQL, linter og formatering (ikke sat op).
- Beregningens regler og beløb (hører ikke til disse opgaver; kun sammenholdt skærm og CSV).
- Rigtige gamle rapporter fra menneskets database: de ligger i den database og mappe, jeg ikke må røre. Jeg har kun efterlignet en gammel rapport ved at ændre snapshottet i min midlertidige database. Den gemte PDF i den efterlignede rapport er ny og indeholder derfor ikke gamle ord.
- Tidligere genåbning i menneskets database (auditloggen "Genåbnede godkendt kørsel" fra første bygning af task-0013): ikke set. Handlingsfilteret i menneskets administration vil derfor muligvis vise både den gamle og den nye tekst ("Genåbnede godkendt kørsel" og "Genåbnede kørsel"); det er historik.
- Samtidige brugere og dobbeltklik.

## Fund

### F1 — En forældet beregning kan godkendes og eksporteres, også efter en ny upload · alvor: middel
**Reproduktion (ingen skærm eller afvisning forhindrer det):**
1. Kør en kørsel til og med Godkend alle. Tryk Genåbn til rettelser. (Kørslen har nu status "beregnet" og beregning 001 er gældende.)
2. Variant A (ny fil): upload en ny fil i trin 1. Kørslen får status "kladde", rækkerne erstattes, og resultaterne i 001 mister deres link til rækkerne. Tryk "4 Godkend" i trinsøjlen. Siden viser stadig beregning 001 med de gamle tal, og alle knapper er aktive. Tryk "Godkend alle": "13 medarbejder(e) godkendt." Kørslen får status "godkendt", Kørsler-siden viser "Godkendt", og eksportadressen leverer CSV med tallene fra den gamle fil. Der er ikke kørt Beregn efter den nye upload.
3. Variant B (rettelse uden Beregn): efter Genåbn, ret en medarbejders transport under Undtagelser (fx taxa til kører selv, 3 zoner) og tryk "Gem kladde" (ikke Beregn). Gå til Godkend: skærmen viser stadig "Taxa" for medarbejderen. "Godkend alle", og eksporten indeholder de gamle beløb for medarbejderen (set: 217,50 i træk, 0,00 i udbetaling, selv om rækken nu er kører selv).
Forventet: en beregning, der ikke længere svarer til rækker, transport og zoner, bør ikke kunne godkendes og eksporteres uden en ny Beregn, eller skærmen bør sige, at den er forældet. Faktisk: ingen kontrol. Variant A fører desuden kørslen fra "kladde" direkte til "godkendt" uden at være "beregnet" i mellemtiden.
**Er det en fejl eller et muligt bevidst valg?** Variant A ser ud som en fejl: statusforløbet kladde, beregnet, godkendt brydes, og CLAUDE.md siger, at godkendelsen hører til en bestemt beregningskørsel og først bortfalder ved en ny Beregn. Variant B kan være bevidst ("godkend det, der blev beregnet"), men så er det ikke synligt for brugeren. Funktionen er ikke ny, men task-0013 forstærker risikoen: efter Genåbn bliver man på Godkend, og beskeden lyder nu "Godkend igen, eller ret oplysningerne under Undtagelser." Den tidligere tekst sagde "Ret oplysningerne og kør en ny beregning, eller godkend igen." Ordene om at køre en ny beregning er væk.
**Hvorfor det betyder noget:** Lønudtrækket er det, der gives videre til lønsystemet. En administrativ medarbejder kan godkende og eksportere tal, der ikke passer til den fil og de rettelser, hun mener at have godkendt, uden at nogen ting på skærmen advarer. Det rammer lønudbetaling (udbetaling og træk i lønart 991), og der er ingen test, der dækker det.
**Forslag:** Beslut, hvad der skal gælde (en opgave til `architect`). Mulige veje: (a) en ny upload eller en gemt rettelse efter beregningen markerer beregningen som forældet, så Godkend alle og eksport er låst, til Beregn er kørt igen, og Godkend-skærmen siger det; (b) som minimum, at `godkend` ikke kan sætte status til "godkendt" fra "kladde"; (c) genindsæt "kør en ny beregning" i beskeden efter Genåbn. En test af den valgte regel mangler.

### F2 — Godkend med et resultatnummer, der ikke er et tal, giver serverfejl · alvor: note
**Reproduktion:** Som logget ind, POST til `/koersel/<pk>/godkend/` med `handling=godkend` og `resultat=abc`. Forventet: besked eller ingen virkning. Faktisk: HTTP 500 (`int(resultat_id)` i `godkend` i `koersel/views.py`). Samme klasse som de to fund, `architect` allerede har afvist for afklar og Opret ny medarbejder (felt `linje`): bekræftet nu også, at `handling=afklar` med `linje=` (tom) og `linje=abc` giver 500. En tom `resultat` godkender alle (bevidst, bruges af "Godkend alle").
**Hvorfor det betyder noget:** Kan kun nås ved en forfalsket anmodning; skærmene sender altid et tal. Ingen sikkerhedsfejl (login kræves).
**Forslag:** Ingen handling nødvendig, hvis den tidligere afvisning gælder; nævnt, fordi det nu er tre steder med samme mønster. Ville kunne samles i én lille opgave med de to afviste.

### F3 — Genåbn uden noget at fjerne giver ingen tilbagemelding · alvor: note
**Reproduktion:** Med en beregnet kørsel og ingen godkendte, tryk "Genåbn til rettelser". Forventet efter opgaven: knappen er altid synlig og kan altid trykkes (opfyldt). Faktisk: siden genindlæses uden besked, uden ændring og uden auditlogpost.
**Er det en fejl eller et muligt bevidst valg?** Bevidst (udviklerens noter: "ingen besked").
**Hvorfor det betyder noget:** Brugeren, der trykker og ikke ser noget, kan tro at knappen er gået i stykker. Konsekvensen er lille.
**Forslag:** En kort besked ("Der var ingen godkendelser at fjerne."), hvis `architect` vil have det.

### F4 — Serverens status for forudfyldte dage viser "Mangler dage", mens feltet står forudfyldt · alvor: note
**Reproduktion:** På Undtagelser, slå individuel beregning til for en medarbejder med dage i filen, lad dagene stå tomme, og tryk "Gem kladde". Siden indlæses igen med feltet forudfyldt (fx 17), men statusmærket i den serverrenderede HTML er "Mangler dage" (og tælleren "klar" tæller ikke rækken). Først `undtagelser.js` ved indlæsning regner statussen om efter det viste tal. Beregn med de viste tal virker (formularen sender de 17).
**Hvorfor det betyder noget:** Uden skærmkode (eller før den kører) viser siden to ting, der ikke passer sammen. Med skærmkode er det ikke synligt. Jeg kan ikke se, om skærmkoden gør det rigtigt, fordi jeg ikke har en browser.
**Forslag:** Ingen handling nødvendig; nævnt for fuldstændighedens skyld. Kan lukkes ved at beregne status i visningen ud fra den forudfyldte værdi.

### F5 — Gamle kørsler viser stadig "borger" på Godkend-skærmen og beregningsgrundlaget · alvor: note
**Reproduktion:** Åbn Godkend-skærmen for en kørsel, hvis beregning blev lavet før task-0007 (jeg efterlignede det med et ændret snapshot). Advarslerne og trinene læses fra snapshotten og viser "borgeren" og "Borgerens …".
**Er det en fejl eller et muligt bevidst valg?** Bevidst og dokumenteret (task-0007: snapshots er uforanderlige; beslutningsloggen). Skrevet her, fordi opgavens kriterium "ingen skærm viser borger" ellers kan læses som opfyldt for alle kørsler.
**Forslag:** Ingen, medmindre `architect` vil oversætte ordene ved visningen (uden at røre snapshottet).

### F6 — Reparationsscriptet finder kun én bestemt karantænetekst og kun `.py.txt` · alvor: note
**Reproduktion:** I en opdigtet `.venv`: en `cache.py.txt` med en anden ordlyd (eller anden stor/lille skrift) i stedet for scriptets sætning, eller en karantænefil med anden endelse (`.pyd.txt`, `.txt`). Forventet efter task-0014 ("tekst om, at filen er sat i karantæne", endelsen `.py.txt`): fundet. Faktisk: ikke fundet; scriptet melder "i orden" og afslutter med 0, hvis Django stadig kan importeres (med en rigtig import fejler den, og så melder scriptet "Det ligner ikke en karantæne", returkode 2 — jeg har kun kørt dette med en indsprøjtet import, ikke med en rigtig).
**Er det en fejl eller et muligt bevidst valg?** Det er i overensstemmelse med opgaven. Den rigtige karantænefil, der opstod i dag, begynder præcis med scriptets sætning (med byte-orden-markør), så for den nuværende tjeneste virker det. Nævnt, fordi en ændring i tjenestens tekst gør scriptet blindt, uden at det siger det højt.
**Forslag:** Ingen handling nødvendig nu. Ændrer tjenesten teksten, bliver et nyt nummer nødvendigt.

### F7 — Ingen test dækker, at en forældet beregning ikke kan godkendes · alvor: note (dækningshul, knyttet til F1)
**Reproduktion:** Læs `koersel/tests.py`: `test_ny_beregning_ophaever_tidligere_godkendelser` dækker Beregn efter godkendelse, men ingen test dækker upload eller rettelse mellem Beregn og godkendelse.
**Forslag:** Følger af, hvad `architect` beslutter under F1.

## Uklart
- **F1:** Er det bevidst, at en beregning kan godkendes og eksporteres, efter at filen eller undtagelserne er ændret uden en ny Beregn? Jeg antog, at variant A (kladde direkte til godkendt) ikke er tilsigtet, og at variant B kan være det.
- **Karantænen i den rigtige `.venv`:** Om menneskets server på port 8000 stadig svarer, og om mennesket vil have reparationsscriptet kørt eller `.venv` bygget forfra, er ikke afgjort af mig. Jeg har ikke undersøgt, hvad der udløste den (den kom ca. fem minutter efter, at jeg startede en server og kørte tests mod `.venv`; det er ikke et bevis for en sammenhæng, og der er ingen grund til at tro, at min kørsel udløste den).
- **Gammel rapport:** Jeg kunne ikke prøve en rigtig gammel rapport og en rigtig gammel PDF (uden for hvad jeg må røre). Det er afprøvet kun med et ændret snapshot.
- **Udseende:** Hele udseendet af knapper og rækker er ikke set af mig og hører til mennesket.

## Afledte numre
task-0015 (fund 1 og 7). Fund 2 til 6 er afvist; se beslutningsloggen.
