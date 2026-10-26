---
nummer: task-0013
titel: Knapperne øverst på Godkend-skærmen i ny rækkefølge, med PDF og eksport låst til alle er godkendt
kilde: interview
status: i-gang
oprettet: 2026-10-26
---

# task-0013 — Knapperne øverst på Godkend-skærmen i ny rækkefølge, med PDF og eksport låst til alle er godkendt

## Hvad og hvorfor
Mennesket vil have knapperne øverst på Godkend-skærmen i en anden rækkefølge og med en tydeligere låsning. I dag står PDF-knappen først og kan altid trykkes, "Godkend alle" i midten, og eksport er en tekst, indtil alle er godkendt. "Genåbn til rettelser" står kun, når kørslen er godkendt.

Den nye rækkefølge fra venstre er: "Godkend alle", "Genåbn til rettelser", "Eksportér lønudtræk (CSV)" og "Åbn PDF-rapport". PDF og eksport er begge knapper, der ikke kan trykkes, før alle medarbejdere er godkendt.

## Færdig når
- [ ] Knapperne øverst står fra venstre i rækkefølgen: "Godkend alle", "Genåbn til rettelser", "Eksportér lønudtræk (CSV)", "Åbn PDF-rapport" med rapportens nummer.
- [ ] "Godkend alle" er altid synlig. Mangler nogen at blive godkendt, kan den trykkes og virker som i dag. Er alle godkendt, er den grøn og kan ikke trykkes, med samme tekst og samme bredde.
- [ ] "Genåbn til rettelser" er altid synlig og kan altid trykkes. Er kørslen godkendt, genåbner den kørslen som i dag. Er den ikke godkendt, fører den til Undtagelser som i dag, uden at ændre noget.
- [ ] "Eksportér lønudtræk (CSV)" er altid en knap. Den kan ikke trykkes, før alle er godkendt. Er alle godkendt, kan den trykkes og henter lønudtrækket som i dag. Teksten "Eksport er låst, til alle medarbejdere er godkendt." er væk.
- [ ] "Åbn PDF-rapport" er altid en knap. Den kan ikke trykkes, før alle er godkendt. Er alle godkendt, kan den trykkes og åbner rapporten i en ny fane som i dag.
- [ ] De knapper, der ikke kan trykkes, forklarer hvorfor, når man holder musen over dem, og forklaringen kan læses op af skærmlæsere. Teksten er "Kan først bruges, når alle medarbejdere er godkendt."
- [ ] Mærket "Godkendt" øverst, ved siden af den gamle knap til genåbning, er væk. Den grønne "Godkend alle" viser samme oplysning.
- [ ] Ingen af knapperne flytter sig eller skifter bredde, når der godkendes, eller når alle er godkendt.
- [ ] Eksporten er stadig låst på serveren, så den ikke kan hentes uden at alle er godkendt, selv med en direkte adresse.
- [ ] Afsnittet "Tidligere beregninger for måneden" er uændret og har stadig sine egne "Åbn PDF"-knapper.
- [ ] Rækkerne med medarbejdere, deres knapper og resten af skærmen er uændret.
- [ ] Der er en test af rækkefølgen, af at PDF og eksport er deaktiverede før og aktive efter, at alle er godkendt, af at "Godkend alle" er grøn og deaktiveret efter, og af at "Genåbn til rettelser" er der i begge tilstande.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- Knapperne står øverst i `templates/koersel/godkend.html`, i rækken `.actions`. Rækkefølgen ændres. De deaktiverede udgaver er knapper uden adresse og uden at kunne trykkes, med en forklaring i titel og i læsbar tekst, på samme måde som de grønne "Godkend"-knapper i rækkerne. De aktive udgaver er links som i dag.
- "Godkend alle" er en formular med en knap. Er alle godkendt, vises den som en grøn, deaktiveret knap med samme tekst, i samme stil som "Godkend" i rækkerne.
- "Genåbn til rettelser" er den eksisterende formular, som nu altid vises. Visningen af godkendelsen håndterer allerede begge tilfælde (den genåbner en godkendt kørsel og fører ellers til Undtagelser), så der skal ikke ændres noget i den.
- Hvornår "alle er godkendt", afgøres som i dag af `kan_eksportere`, som er den samme regel, eksporten bruger.
- Stilen følger de eksisterende knapper. Tjek at ingen regel får knapperne til at skifte bredde mellem de to udgaver.

## Hvad vi ikke rører
- Godkendelseslogikken, genåbning, eksportens indhold og PDF-rapporten.
- Rækkerne med medarbejdere og deres knapper.
- "Tidligere beregninger for måneden".
- Alle andre skærme.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Rækkefølgen er "Godkend alle", "Genåbn til rettelser", "Eksport", "PDF" — mennesket bestemte den.
- BESLUTTET: "Genåbn til rettelser" er altid synlig og klikbar — mennesket bad om det. Visningen håndterer det allerede.
- BESLUTTET: "Godkend alle" bliver grøn og deaktiveret, når alle er godkendt, og mærket "Godkendt" øverst fjernes — samme mønster som knapperne i rækkerne, så intet flytter sig. Valget er architects og kan vendes. Afvist: at skjule knappen, som ville flytte de andre.
- BESLUTTET: PDF-låsen gælder kun knappen på denne skærm — rapporten kan stadig åbnes fra listen over tidligere beregninger. Eksporten er låst på serveren i forvejen.
- BESLUTTET: Forklaringen på de låste knapper er en titel og en læsbar tekst — ellers ved brugeren ikke hvorfor knappen ikke virker.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
- `templates/koersel/godkend.html`: knapperne i `.actions` står nu i rækkefølgen "Godkend alle", "Genåbn til rettelser", "Eksportér lønudtræk (CSV)", "Åbn PDF-rapport <nummer>". Alle fire er altid synlige. "Alle godkendt" afgøres af `kan_eksportere` for alle fire (samme regel som eksporten).
- "Godkend alle": formular med knap, når `kan_eksportere` er falsk. Ellers `<button type="button" disabled class="godkendt">` med samme tekst, title og aria-label "Alle medarbejdere er godkendt.".
- "Genåbn til rettelser": den eksisterende formular, nu altid vist og aktiv. `koersel/views.py` er ikke rørt.
- Eksport og PDF: links (`a.btn`, PDF med `target="_blank" rel="noopener"`) når alle er godkendt; ellers deaktiverede knapper med samme tekst (PDF inkl. rapportnummer), title og aria-label "Kan først bruges, når alle medarbejdere er godkendt.". Teksten "Eksport er låst, til alle medarbejdere er godkendt." og mærket "Godkendt" (badge ok) øverst er fjernet.
- `static/css/app.css`: reglen for den grønne knap gælder nu også `.actions button.godkendt` (samme padding og kant som rækkernes, så samme bredde). Ny regel for deaktiverede knapper øverst (`.actions button:disabled:not(.godkendt)`: appens egne farvevariabler, `cursor: default`, dæmpet). Ingen nye kommandoer eller indstillinger.
- `koersel/tests.py`: ny test `test_knapperne_oeverst_staar_i_ny_raekkefoelge_og_er_laast_til_alle_er_godkendt` (rækkefølge; før godkendelse og med én godkendt: PDF og eksport er deaktiverede knapper uden href, "Godkend alle" aktiv, eksportadressen afviser; efter "Godkend alle": links, grøn deaktiveret "Godkend alle", intet mærke, ingen "Eksport er låst"; "Genåbn til rettelser" aktiv i alle tilstande, også efter genåbning). Rettet to eksisterende tests der pegede på den gamle tekst "Eksport er låst" og på mærket øverst (nu forventet væk).
- Kørt: `manage.py test` én gang for hele suiten: "Ran 94 tests ... OK". `makemigrations --check`: "No changes detected".

### Hvad er ikke lavet, og hvorfor
- Udseendet (bredde, placering, farver i lys og mørk tilstand, hover) er ikke efterprøvet visuelt; ingen browser er startet. Bredden er sikret ved samme tekst, samme klasse-padding og samme kant, men ikke set.
- Ellers intet.

### Uklart
intet
