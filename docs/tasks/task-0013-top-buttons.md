---
nummer: task-0013
titel: Knapperne øverst på Godkend-skærmen i ny rækkefølge, med PDF og eksport låst til alle er godkendt
kilde: interview
status: afsluttet
oprettet: 2026-10-26
---

# task-0013 — Knapperne øverst på Godkend-skærmen i ny rækkefølge, med PDF og eksport låst til alle er godkendt

## Hvad og hvorfor
Mennesket vil have knapperne øverst på Godkend-skærmen i en anden rækkefølge og med en tydeligere låsning. I dag står PDF-knappen først og kan altid trykkes, "Godkend alle" i midten, og eksport er en tekst, indtil alle er godkendt. "Genåbn til rettelser" står kun, når kørslen er godkendt.

Den nye rækkefølge fra venstre er: "Godkend alle", "Genåbn til rettelser", "Eksportér lønudtræk (CSV)" og "Åbn PDF-rapport". PDF og eksport er begge knapper, der ikke kan trykkes, før alle medarbejdere er godkendt.

## Færdig når
- [ ] Knapperne øverst står fra venstre i rækkefølgen: "Godkend alle", "Genåbn til rettelser", "Eksportér lønudtræk (CSV)", "Åbn PDF-rapport" med rapportens nummer.
- [ ] "Godkend alle" er altid synlig. Mangler nogen at blive godkendt, kan den trykkes og virker som i dag. Er alle godkendt, er den grøn og kan ikke trykkes, med samme tekst og samme bredde.
- [ ] "Genåbn til rettelser" er altid synlig og kan altid trykkes. Trykkes den, fjernes godkendelsen af alle medarbejdere på den gældende beregning, så alle "Godkend"-knapper er tilbage som ikke godkendt, og ingen er grønne. Man bliver på Godkend-skærmen, så man ser knapperne skifte tilbage, og en kort besked siger, at kørslen er genåbnet, og hvor mange godkendelser der er fjernet. Det gælder, uanset om alle eller kun nogle er godkendt.
- [ ] Er kørslen godkendt, genåbnes den som i dag, så eksport og PDF låses igen. Hvem der godkendte, og hvornår, er ryddet på de medarbejdere, hvis godkendelse er fjernet.
- [ ] Genåbningen står i auditloggen, som i dag, og siger, hvor mange godkendelser der blev fjernet.
- [ ] Efter genåbningen står alle medarbejdere som ikke godkendt på Godkend-skærmen, uden at man har kørt "Beregn" igen, og "Godkend alle" er aktiv.
- [ ] Trinsøjlens knap til Undtagelser er stadig den vej, man bruger til at rette oplysninger. Genåbning fører ikke længere til Undtagelser af sig selv.
- [ ] "Eksportér lønudtræk (CSV)" er altid en knap. Den kan ikke trykkes, før alle er godkendt. Er alle godkendt, kan den trykkes og henter lønudtrækket som i dag. Teksten "Eksport er låst, til alle medarbejdere er godkendt." er væk.
- [ ] "Åbn PDF-rapport" er altid en knap. Den kan ikke trykkes, før alle er godkendt. Er alle godkendt, kan den trykkes og åbner rapporten i en ny fane som i dag.
- [ ] De knapper, der ikke kan trykkes, forklarer hvorfor, når man holder musen over dem, og forklaringen kan læses op af skærmlæsere. Teksten er "Kan først bruges, når alle medarbejdere er godkendt."
- [ ] Mærket "Godkendt" øverst, ved siden af den gamle knap til genåbning, er væk. Den grønne "Godkend alle" viser samme oplysning.
- [ ] Ingen af knapperne flytter sig eller skifter bredde, når der godkendes, eller når alle er godkendt.
- [ ] Eksporten er stadig låst på serveren, så den ikke kan hentes uden at alle er godkendt, selv med en direkte adresse.
- [ ] Afsnittet "Tidligere beregninger for måneden" er uændret og har stadig sine egne "Åbn PDF"-knapper.
- [ ] Rækkerne med medarbejdere, deres knapper og resten af skærmen er uændret.
- [ ] Der er en test af rækkefølgen, af at PDF og eksport er deaktiverede før og aktive efter, at alle er godkendt, af at "Godkend alle" er grøn og deaktiveret efter, af at "Genåbn til rettelser" er der i begge tilstande, og af at ingen godkendelser er tilbage efter genåbning, både når alle og når kun nogle var godkendt.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- Knapperne står øverst i `templates/koersel/godkend.html`, i rækken `.actions`. Rækkefølgen ændres. De deaktiverede udgaver er knapper uden adresse og uden at kunne trykkes, med en forklaring i titel og i læsbar tekst, på samme måde som de grønne "Godkend"-knapper i rækkerne. De aktive udgaver er links som i dag.
- "Godkend alle" er en formular med en knap. Er alle godkendt, vises den som en grøn, deaktiveret knap med samme tekst, i samme stil som "Godkend" i rækkerne.
- "Genåbn til rettelser" er den eksisterende formular, som nu altid vises. Handlingen i visningen ændres: ud over at genåbne en godkendt kørsel fjerner den godkendelsen af alle medarbejdere på den gældende beregning (godkendt, hvem og hvornår), skriver antallet i auditloggen og omdirigerer tilbage til Godkend-skærmen, ikke til Undtagelser. Den hører til det, der ellers ikke røres, men er en bevidst undtagelse.
- Hvornår "alle er godkendt", afgøres som i dag af `kan_eksportere`, som er den samme regel, eksporten bruger.
- Stilen følger de eksisterende knapper. Tjek at ingen regel får knapperne til at skifte bredde mellem de to udgaver.

## Hvad vi ikke rører
- Godkendelseslogikken for at godkende, eksportens indhold og PDF-rapporten. Genåbningen ændres som beskrevet ovenfor og ellers ikke.
- Rækkerne med medarbejdere og deres knapper.
- "Tidligere beregninger for måneden".
- Alle andre skærme.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Rækkefølgen er "Godkend alle", "Genåbn til rettelser", "Eksport", "PDF" — mennesket bestemte den.
- BESLUTTET: "Genåbn til rettelser" er altid synlig og klikbar — mennesket bad om det.
- BESLUTTET: Efter genåbningen bliver man på Godkend-skærmen — mennesket svarede ja til det, fordi det ellers ikke kan ses, at knapperne skifter. Afvist: at føre til Undtagelser, som det hele tiden har gjort. Trinsøjlen fører stadig til Undtagelser.
- BESLUTTET: Genåbn fjerner alle godkendelser på den gældende beregning, også når kun nogle var godkendt — mennesket bad om, at alle grønne knapper går tilbage. Konsekvensen er, at et tryk på Genåbn fra en delvist godkendt kørsel også sletter de godkendelser, der var givet. Det er architects tolkning af ønsket og kan vendes. Afvist: kun at fjerne godkendelserne, når hele kørslen var godkendt.
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

**Udvidelse: Genåbn til rettelser fjerner alle godkendelser (commit 8d3ab1b)**
- `koersel/services.py`: ny funktion `genaabn(beregning, bruger)`, atomisk. Sætter `godkendt=False`, `godkendt_af=None`, `godkendt_tidspunkt=None` på alle godkendte resultater på den gældende beregning i én opdatering. Sætter kørslens status til beregnet, hvis den var godkendt (som før). Skriver auditlogpost og returnerer (antal fjernede, om kørslen var godkendt).
- `koersel/views.py`: handlingen `genaabn` i `godkend` kalder `services.genaabn` og fører til Undtagelser som før. Besked: "Kørslen er genåbnet. N godkendelser er fjernet. Ret oplysningerne og kør en ny beregning, eller godkend igen." (ental: "1 godkendelse er fjernet"). Var kørslen godkendt uden at antallet er over 0 (kan ikke ske i praksis), kommer den gamle besked. Uden godkendelser og uden godkendt kørsel: ingen besked. Uden gældende beregning er visningen uændret (omdirigerer før handlingen).
- Auditlog: handlingen hedder nu "Genåbnede kørsel" (før "Genåbnede godkendt kørsel"; teksten passede ikke, når kun nogle var godkendt). Detaljer: "<kørselsnavn>, fjernede godkendelser: N". Valget om hvornår der logges: der logges kun, hvis kørslen var godkendt eller N er over 0. Et tryk uden effekt fylder ikke loggen.
- Skabelonen er uændret. Efter genåbning er `koersel.status` beregnet og alle `r.godkendt` falske, så rækkens Godkend er aktiv, "Godkend alle" er aktiv (`kan_eksportere` er falsk), og PDF og eksport er låst. Det er efterprøvet i testene.
- `koersel/tests.py`: seks nye tests: helt godkendt kørsel (alle tre felter ryddet, status beregnet, ingen ny beregning, eksport afviser, ingen grønne rækkeknapper, "Godkend alle" aktiv, PDF og eksport låst, kan godkendes igen); delvist godkendt (den givne godkendelse fjernes); antal i auditloggen (både helt og delvist godkendt); genåbn uden godkendelser ændrer ingenting og logger ikke; genåbn før nogen beregning er kørt giver ingen fejl; genåbn kræver login og fjerner intet. De eksisterende tests, der kalder `genaabn`, kræver ikke ændring: de antager ikke, at rækkerne forbliver godkendte.
- Konsekvens, bevidst og skrevet i opgaven: et tryk på Genåbn fra en delvist godkendt kørsel sletter også de godkendelser, der var givet.
- Kørt: `manage.py test` én gang for hele suiten: "Ran 100 tests in 18.005s ... OK" (100 tests, alle grønne). `makemigrations --check`: "No changes detected".

**Rettelse: genåbning bliver på Godkend-skærmen (efter 8d3ab1b)**
- `koersel/views.py`: handlingen `genaabn` i `godkend` omdirigerer nu til `godkend` (`redirect("godkend", pk=pk)`) i stedet for til Undtagelser. Det afløser to punkter ovenfor, hvor commit 8d3ab1b stadig førte til Undtagelser. Uden gældende beregning er visningen uændret (omdirigerer til Undtagelser før handlingen).
- Beskeden er ændret til: "Kørslen er genåbnet. N godkendelser er fjernet. Godkend igen, eller ret oplysningerne under Undtagelser." (ental: "1 godkendelse er fjernet"). Var kørslen godkendt uden at antallet er over 0: "Kørslen er genåbnet. Godkend igen, eller ret oplysningerne under Undtagelser." Uden godkendelser og uden godkendt kørsel: ingen besked, brugeren bliver på Godkend.
- `koersel/tests.py`: tre tests rettet fra omdirigering til Undtagelser til omdirigering til Godkend (helt godkendt, delvist godkendt, uden godkendelser) med den nye besked. Testen for helt godkendt kørsel tjekker nu selve svaret efter omdirigeringen: ingen knap med klassen godkendt i rækkerne eller øverst, "Godkend alle" aktiv, ingen eksportadresse og forklaringen på låst PDF/eksport, og beskeden vises. Testen for genåbning før en beregning er kørt er uændret (Undtagelser).
- Kørt: `manage.py test` én gang for hele suiten: "Ran 100 tests in 20.460s ... OK" (100 tests, alle grønne). `makemigrations --check`: "No changes detected". Ingen browser startet.

### Hvad er ikke lavet, og hvorfor
- Udseendet (bredde, placering, farver i lys og mørk tilstand, hover) er ikke efterprøvet visuelt; ingen browser er startet. Bredden er sikret ved samme tekst, samme klasse-padding og samme kant, men ikke set. Det samme gælder, hvordan Godkend-skærmen ser ud efter genåbning.
- Opgavefilen er ikke committet i denne omgang (kun kode og tests), fordi den har ucommittede ændringer fra architect over delelinjen. Mine noter ligger derfor ucommittet sammen med dem.
- Ellers intet.

### Uklart
intet
