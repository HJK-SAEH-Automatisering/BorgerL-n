---
nummer: task-0006
titel: Beregningsgrundlag som knap og egen side på Godkend-skærmen
kilde: interview
status: afsluttet
oprettet: 2026-10-26
---

# task-0006 — Beregningsgrundlag som knap og egen side på Godkend-skærmen

## Hvad og hvorfor
På Godkend-skærmen står "Se beregningsgrundlag" som en foldet tabel under hver borger. Mennesket mener, at den forvirrer mere, end den gavner, der hvor den står. I stedet skal hver borger have en knap til højre for "Godkend", som åbner beregningsgrundlaget for netop den borger på en ny side.

## Færdig når
- [ ] Teksten "Se beregningsgrundlag" og den foldede tabel er væk fra rækkerne på Godkend-skærmen.
- [ ] Hver borger har en knap, der hedder "Beregningsgrundlag", til højre for "Godkend". Er borgeren allerede godkendt, står knappen stadig yderst til højre, på samme sted.
- [ ] Trykkes knappen, åbner beregningsgrundlaget for netop den borger på en ny side i en ny fane. Godkend-skærmen bliver stående, som den var.
- [ ] Den nye side viser borgerens navn, Tj.nr., afdeling, timer og transport, og beregningsgrundlaget som en tabel med de samme trin og noter som i dag.
- [ ] Siden viser ikke CPR-nummer eller adresse.
- [ ] Siden kræver login, som de øvrige skærme. Et ugyldigt nummer, eller en borger der ikke hører til den gældende beregning, giver "ikke fundet".
- [ ] Godkend, Godkend alle, advarslerne under rækkerne og resten af skærmen er uændrede.
- [ ] Der er tests: siden åbner for en borger og viser tabellen, siden giver "ikke fundet" for et ugyldigt nummer, siden kræver login, og Godkend-skærmen har ikke længere "Se beregningsgrundlag", men har knappen.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- **Ny side.** En ny adresse og visning i `koersel`, der slår borgerens resultat op i den gældende beregning og viser dets beregningsgrundlag. Resultatet har allerede en måde at hente grundlaget på, som den foldede tabel bruger i dag. Siden får sin egen skabelon, som bygger på den fælles grundskabelon og uden trinsøjle, fordi den ikke er et af de fire trin.
- **Knappen.** Knappen er et link, der åbner i en ny fane på samme måde som PDF-knappen. Rækken på Godkend-skærmen får en kolonne mere til knappen; rækkens opbygning i `static/css/app.css` justeres.
- **Fjernes.** Den foldede tabel i `templates/koersel/godkend.html`. Stilarter der kun hørte til den, fjernes, hvis de ikke bruges andre steder.
- **Advarslerne** bliver på Godkend-skærmen under rækken, som i dag. De flyttes ikke til den nye side.

## Hvad vi ikke rører
- Beregningsmotoren, gemte beregninger, PDF-rapport og eksport.
- Godkendelseslogikken: pr. borger, godkend alle, genåbn og låsning af eksport.
- Advarsler, listen pr. borger og "Tidligere beregninger for måneden".
- Alle andre skærme, inklusive trinsøjlen.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Den nye side åbner i en ny fane — som PDF-knappen, uden skærmkode, og Godkend-skærmen bliver, som den er. Afvist: en overlejret rude, som kræver skærmkode.
- BESLUTTET: Den nye side har ingen trinsøjle og ingen godkendelsesknap — den er kun til at læse, og godkendelsen sker på Godkend-skærmen.
- BESLUTTET: Advarslerne bliver på Godkend-skærmen — de skal ses, når man godkender, og ikke gemmes bag en knap.
- BESLUTTET: Knappen hedder "Beregningsgrundlag" — det er menneskets eget ord for funktionen.
- BESLUTTET: Siden viser kun den gældende beregning — tidligere beregninger har deres PDF-rapport.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
Alt på grenen `task-0006-calculation-basis-page`, én commit.
- Foldet tabel og teksten "Se beregningsgrundlag" fjernet fra rækkerne: `templates/koersel/godkend.html`.
- Knap "Beregningsgrundlag" i en ny kolonne yderst til højre for "Godkend". Den står i sin egen celle, som altid vises, så den står samme sted når borgeren er godkendt. Link med `target="_blank" rel="noopener"`: `templates/koersel/godkend.html`. Rækken har fået en syvende kolonne (150px): `.g4` i `static/css/app.css`.
- Ny adresse `koersel/<pk>/grundlag/<resultat>/` (navn `grundlag`): `koersel/urls.py`. Visning `grundlag` med `@login_required`: `koersel/views.py`. Den slår resultatet op i kørslens gældende beregning. Giver 404 ved ukendt kørsel, ingen beregning endnu, ukendt resultatnummer, eller et resultat der hører til en tidligere beregning.
- Ny skabelon `templates/koersel/grundlag.html`: bygger på `base.html`, uden trinsøjle (hverken `stepper` eller `sideclass`) og uden godkendelsesknap. Viser navn, Tj.nr., afdeling, timer, transport (og zoner, som rækken i dag) og tabellen Nr./Trin/Formel/Indsat/Resultat med noter. Ingen CPR og ingen adresse.
- Fjernet stilarterne `details` og `details summary` fra `static/css/app.css`. Tjekket først: ingen andre skabeloner eller scripts bruger `<details>`/`<summary>`.
- Advarslerne under rækkerne er uændrede.
- Tests i `koersel/tests.py` (FlowTests): `test_godkend_skaermen_har_knap_til_beregningsgrundlag_i_stedet_for_foldet_tabel`, `test_beregningsgrundlag_viser_borger_og_tabel_uden_cpr_og_adresse`, `test_beregningsgrundlag_giver_ikke_fundet_for_ugyldigt_nummer_eller_fremmed_borger`, `test_beregningsgrundlag_kraever_login`. Ét eksisterende testkommentar (i `test_godkend_skaermen_har_ikke_rapportlinje_forklaring_eller_totaler`) sagde at beregningsgrundlaget "skal blive" pr. borger på skærmen; kun kommentaren er rettet til at siden nu har sin egen side. Ingen eksisterende test kontrollerede den foldede tabel, så ingen påstande er ændret.
- Suiten: `.venv\Scripts\python.exe manage.py test` gav "Ran 77 tests ... OK" (alle 77 grønne). `makemigrations --check` gav "No changes detected".
- Ny adresse og knap til README: en bruger ser nu knappen "Beregningsgrundlag" ud for hver borger på Godkend-skærmen. Den åbner en skrivebeskyttet side i en ny fane med borgerens trin for trin-beregning.

### Hvad er ikke lavet, og hvorfor
- Udseendet er ikke efterprøvet visuelt (ingen browser startet). Kun HTML'en er kontrolleret i tests: knappens link, at den foldede tabel er væk, og sidens indhold. Om de syv kolonner i rækken og knappens bredde (150px) ser rigtige ud, skal ses af en person.
- Ellers intet.

### Uklart
intet
