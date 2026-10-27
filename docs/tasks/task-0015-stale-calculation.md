---
nummer: task-0015
titel: En forældet beregning kan ikke godkendes eller eksporteres
kilde: test-0004
status: i-gang
oprettet: 2026-10-27
---

# task-0015 — En forældet beregning kan ikke godkendes eller eksporteres

## Hvad og hvorfor
Testrunden `test-0004` viste, at en beregning kan godkendes og eksporteres, selv om fil eller rettelser er ændret, siden den blev kørt. Efter Genåbn og en ny upload kan man trykke "Godkend alle" uden "Beregn", og kørslen bliver godkendt med de gamle tal. Det samme gælder rettelser, der kun er gemt som kladde. Lønudtrækket er det, der gives videre til lønsystemet, så tallene skal svare til den fil og de rettelser, man har set. Mennesket har besluttet, at en forældet beregning skal låses.

## Færdig når
- [ ] En beregning er forældet, når der er uploadet en ny fil, eller når rettelser er gemt, efter at beregningen blev kørt: "Gem kladde" på Undtagelser og "Gem og fortsæt" på Gennemse transport. En ny "Beregn" gør beregningen aktuel igen.
- [ ] På Godkend-skærmen står en tydelig besked øverst, når beregningen er forældet: der er ændret noget, siden den blev kørt, og man skal køre "Beregn" igen under Undtagelser, før man kan godkende. Beskeden har et link til Undtagelser.
- [ ] Er beregningen forældet, kan ingen "Godkend"-knap og ikke "Godkend alle" trykkes, og de står som ikke trykbare knapper, ikke grønne. PDF og eksport kan heller ikke trykkes. "Genåbn til rettelser" og "Beregningsgrundlag" kan stadig trykkes.
- [ ] Serveren afviser også en godkendelse af en forældet beregning, selv med en forfalsket anmodning. Der godkendes intet, og brugeren får samme besked.
- [ ] Eksport er stadig låst på serveren, så den ikke kan hentes for en forældet beregning.
- [ ] En kørsel går ikke direkte fra kladde til godkendt. Den skal være beregnet først.
- [ ] Efter en ny "Beregn" er alt som i dag: godkendelserne bortfalder, man kan godkende, og eksport og PDF åbner, når alle er godkendt.
- [ ] Beskeden efter "Genåbn til rettelser" nævner igen, at man skal køre en ny beregning, hvis man retter noget: "Kørslen er genåbnet. N godkendelser er fjernet. Godkend igen, eller ret oplysningerne under Undtagelser og kør en ny beregning."
- [ ] Er der ingen forældet beregning, ser Godkend-skærmen og alle knapper ud og virker som i dag.
- [ ] Der er tests: ny upload efter genåbning, "Gem kladde" og "Gem og fortsæt" efter beregning gør beregningen forældet; godkend og "Godkend alle" afvises både på skærmen og på serveren; eksport er låst; en ny "Beregn" gør alt aktuelt igen; kørslen går aldrig fra kladde til godkendt; beskeden efter genåbning er rettet.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- **Hvornår er en beregning forældet.** Kørslens status bruges. Upload sætter den i dag til kladde. "Gem kladde" på Undtagelser og "Gem og fortsæt" på Gennemse skal også sætte den til kladde, når der findes en beregning. Er status kladde, og der findes en beregning, er beregningen forældet. "Beregn" sætter den til beregnet, som i dag. Er kørslen godkendt, er skærmene låst i forvejen, så den ikke kan ændres.
- **Godkendelse.** Serveren afviser godkendelse af en forældet beregning, i funktionen der godkender, så den også gælder en forfalsket anmodning. Visningen viser beskeden i stedet for at godkende.
- **Godkend-skærmen.** Skabelonen får en besked øverst, når beregningen er forældet, og knapperne vises som ikke trykbare ved at bruge det samme mønster som i dag (en knap, der ikke kan trykkes, med en forklaring ved musen og til skærmlæsere). Genåbn og Beregningsgrundlag er uændrede.
- **Genåbn.** Teksten i beskeden rettes.
- **Eksport.** Den afgøres allerede af kørslens status og af at alle er godkendt; tjek, at en forældet beregning ikke kan komme til at passere.
- **Ingen ny model og ingen migrering**, medmindre det viser sig nødvendigt; så skrives det i noterne.

## Hvad vi ikke rører
- Beregningsmotoren, snapshot, PDF-rapport og eksportens indhold.
- Upload, import, matchning og reglerne for hvornår en række er klar.
- Rækkernes og knappernes udseende, ud over at de ikke kan trykkes, når beregningen er forældet.
- Alle andre skærme.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: En forældet beregning låses for godkendelse og eksport — mennesket besluttede det. Afvist: at lade det være som i dag, hvor lønudtrækket kan indeholde de gamle tal.
- BESLUTTET: Enhver gemt rettelse efter beregningen gør den forældet, også en "Gem kladde" uden nogen ændring — det er enkelt og kræver ingen sammenligning af data. Konsekvensen er, at man skal køre "Beregn" igen efter et "Gem kladde". Det er architects valg og kan vendes. Afvist: kun at markere, når noget faktisk er ændret.
- BESLUTTET: Beskeden og knapperne følger de mønstre, der findes — ingen nye farver eller nye knapper.
- BESLUTTET: Opgaven samler fund 1 og 7 fra `test-0004`. De andre fund er afvist i beslutningsloggen.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
- Forældet beregning (punkt 1): `koersel/models.py` har ny egenskab `Koersel.beregning_foraeldet` (status kladde og der findes en beregning). `koersel/services.py` har ny `goer_foraeldet(koersel)`, der sætter beregnet til kladde. `koersel/views.py` kalder den ved "Gem kladde" (undtagelser, og ved enhver anden gemning i undtagelser, se nedenfor), "Gem og fortsæt" (gennemse, handlingen `gem`) og "Afklar". Upload sætter allerede kladde. Ny "Beregn" sætter beregnet som før.
- Besked og knapper (punkt 2, 3): `templates/koersel/godkend.html` har en `alertbox` øverst ("Beregningen er forældet. Der er ændret noget, siden den blev kørt. Kør Beregn igen under Undtagelser, før du kan godkende." med link til Undtagelser). Visningen `godkend` sender `foraeldet` til skabelonen. Er den sand, er "Godkend alle" og alle rækkernes "Godkend" deaktiverede knapper uden klassen `godkendt` (titel og aria-label "Beregningen er forældet. Kør Beregn igen."). Eksport og PDF er deaktiverede med samme forklaring i stedet for "Kan først bruges, når alle medarbejdere er godkendt.". Genåbn og Beregningsgrundlag er uændrede. Ingen CSS er ændret.
- Server (punkt 4, 6): `services.godkend` afviser med ny undtagelse `services.BeregningForaeldet`, når kørslens status i databasen er kladde, før noget godkendes. Slutopdateringen til godkendt kræver nu status beregnet, så kørslen ikke kan gå fra kladde til godkendt. Visningen `godkend` fanger undtagelsen og viser `messages.error` med samme tekst som banneret. Gælder både "Godkend" pr. række, "Godkend alle" og direkte POST.
- Eksport (punkt 5): ingen kodeændring. `kan_eksportere` og `eksport` kræver status godkendt, så en forældet beregning (kladde) afvises. Dækket af test.
- Genåbn (punkt 8): beskeden i `koersel/views.py` er nu "Kørslen er genåbnet. N godkendelser er fjernet. Godkend igen, eller ret oplysningerne under Undtagelser og kør en ny beregning." (ental og uden antal som før). De to eksisterende tests med den gamle tekst er rettet i `koersel/tests.py`.
- Tests (punkt 10): 12 nye tests i `koersel/tests.py` (FlowTests): ny upload efter genåbning, Gem kladde, Gem og fortsæt, afvist Beregn med gemte rettelser, Afklar (og ugyldigt valg ændrer intet), "Fortsæt" uden at gemme ændrer intet; godkend pr. række, godkend alle og tom `resultat` afvises på skærmen og ved direkte POST (ingen godkendelser, status uændret, ingen auditlinje, eksport afvist); Genåbn og Beregningsgrundlag virker for en forældet beregning; ny Beregn gør alt aktuelt igen (godkend, eksport og PDF åbner); kladde går aldrig til godkendt (service og visning); ikke-forældet beregning virker som før; kladde uden beregning er ikke forældet.
- Punkt 9 (uændret skærm uden forældet): de eksisterende skærmtests er uændrede og grønne, bortset fra de to beskedtekster.
- Resultat: `.venv\Scripts\python.exe manage.py test` gav "Ran 135 tests in 26.838s ... OK" (alle 135 grønne). `makemigrations --check` gav "No changes detected". Linter findes ikke.
- Commits på grenen `task-0015-stale-calculation`: kode og rettede tests (b19babe), nye tests.
- Til README: ingen nye kommandoer eller indstillinger. Brugerens synlige ændring: en forældet beregning (efter ny upload, Gem kladde eller Gem og fortsæt) kan ikke godkendes eller eksporteres, før "Beregn" er kørt igen; Godkend-skærmen siger det.

### Hvad er ikke lavet, og hvorfor
- Udseendet er ikke efterprøvet visuelt (ingen browser startet): bannerets udseende, at de deaktiverede rækkeknapper ikke skifter plads eller bredde, og at den grå tilstand ser rigtig ud. Kun HTML'en er prøvet i tests. Rækkeknapperne bruger kun browserens standardudseende for deaktiverede knapper (ingen ny CSS); topknapperne får den eksisterende grå stil `.actions button:disabled:not(.godkendt)`.
- Intet er blokeret. Ingen spærring eller karantæne i `.venv` mødt; `.venv` virkede hele vejen.

### Uklart
- Afklar (valgt): "Afklar" gør også beregningen forældet. Begrundelse: den ændrer hvilken medarbejder rækken hører til og nulstiller transport, zoner og individuel beregning (`Linje.saet_borger`), så en gammel beregning ikke længere passer. I almindeligt brug sker det kun efter en ny upload (da er kørslen allerede kladde), så det gør i praksis kun forskel ved en forfalsket anmodning. Kan fjernes, hvis du hellere vil holde dig til de to nævnte handlinger.
- Afvist Beregn (tilføjet ud over ordlyden): `undtagelser` gemmer rettelserne, før Beregn prøves. Fejler Beregn (manglende zone m.m.), står rettelserne gemt, og den gamle beregning ville ellers stadig være "beregnet" og kunne godkendes med gamle tal. Derfor kaldes `goer_foraeldet` lige efter gemningen, uanset om handlingen er Gem kladde eller Beregn. Er det for vidt, kan kaldet flyttes ind i grenen for Gem kladde.
- Godkendt række i forældet beregning: er en række allerede godkendt (delvis godkendelse, derefter ny upload uden Genåbn), vises den også som grå deaktiveret "Godkend" med forældet-forklaring, ikke grøn "Godkendt af ...". Godkendelsen fjernes ikke af upload; Genåbn fjerner den. Er det ikke ønsket, skal opgaven afgøre det.
- Beskeden efter Genåbn siger "Godkend igen, eller ret ... og kør en ny beregning", også når kørslen er forældet og "Godkend igen" ikke kan lade sig gøre. Teksten er den, opgaven foreskriver; bannerets besked står samtidig øverst.
- "Gem og fortsæt" markerer som forældet, også når alle rækker afvises og intet blev gemt (konservativt, i tråd med beslutningen om at enhver gemning gør den forældet).
- Fund uden for opgaven: intet. F2 (500 ved resultatnummer der ikke er et tal) er uændret og stadig afvist.
