---
nummer: task-0005
titel: Simplificér Godkend-skærmen
kilde: interview
status: afsluttet
oprettet: 2026-10-26
---

# task-0005 — Simplificér Godkend-skærmen

## Hvad og hvorfor
Mennesket har gennemgået Godkend-skærmen og vil simplificere den. For meget information og for mange knapper gør den tungere at overskue, og tre ting er ikke nødvendige. Opgaven fjerner dem uden at røre det, der bruges til at godkende.

## Færdig når
- [ ] Linjen øverst til højre med rapportnummer, tidspunkt og "x af y godkendt" er væk fra skærmen.
- [ ] Sætningen under overskriften, "Gennemgå, hvordan beløbet er beregnet for hver borger. Intet kan eksporteres, før alle borgere er godkendt.", er væk.
- [ ] Rækken med de fem totaler (Borgere, Løn før skat, Løn efter skat, Træk, Udbetaling) er væk.
- [ ] Overskriften "Godkend beregning" med månedens navn står stadig.
- [ ] Knappen til PDF-rapporten, som nævner rapportens nummer, findes stadig og virker.
- [ ] "Godkend alle" findes stadig og virker. Er alt godkendt, vises "Godkendt" og "Genåbn til rettelser", som i dag.
- [ ] Er der ikke godkendt alt, står teksten "Eksport er låst, til alle borgere er godkendt.", og knappen til eksport findes først, når alt er godkendt. Det virker som i dag.
- [ ] "Tilbage til undtagelser" findes stadig.
- [ ] Listen "Beregning pr. borger" er uændret, med godkend pr. borger, advarsler og beregningsgrundlag.
- [ ] Afsnittet "Tidligere beregninger for måneden" er uændret.
- [ ] Skærmen virker uden fejl både før og efter, at alt er godkendt.
- [ ] Der er ikke bygget noget nyt, og ingen andre skærme er ændret.
- [ ] Tests, der kontrollerer de fjernede dele, er rettet. Der er en test, der viser, at de tre ting ikke længere står på skærmen.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- Skærmens skabelon er `templates/koersel/godkend.html`. De tre dele fjernes dér.
- Det der kun blev brugt af de fjernede dele, fjernes også, hvis det ikke bruges andre steder: de værdier visningen i `koersel/views.py` sender med til skabelonen (totalerne og antallet af godkendte), og de stilarter i `static/css/app.css`, der kun hørte til totalrækken. Tjek først, at de ikke bruges af andre skærme, fx forsiden. Er de i brug, lades de stå.
- Totalerne findes stadig i beregningens gemte data og i PDF-rapporten og eksporten. Det rører vi ikke.

## Hvad vi ikke rører
- Beregningsmotoren, gemte beregninger, PDF-rapport og eksport.
- Godkendelseslogikken: pr. borger, godkend alle, genåbn og låsning af eksport.
- Listen pr. borger og beregningsgrundlaget.
- Alle andre skærme, inklusive trinsøjlen.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: De tre markerede dele fjernes, og alt andet på skærmen bliver — mennesket markerede dem som unødvendige på et skærmbillede. Afvist: at fjerne flere ting uden at spørge.
- BESLUTTET: Totalerne fjernes kun fra skærmen, ikke fra rapporten og eksporten — mennesket bad kun om en enklere skærm.
- BESLUTTET: Ubrugt kode, der kun hørte til de fjernede dele, fjernes — så der ikke efterlades døde dele. Er den i brug andre steder, bliver den stående.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
Alt på grenen `task-0005-simplify-approval`, commit `df83408`.
- `templates/koersel/godkend.html`: fjernet (1) linjen med rapportnummer, tidspunkt og "x af y godkendt" i `.head`, (2) sætningen "Gennemgå, hvordan beløbet er beregnet…", (3) rækken `.tiles` med de fem totaler. Overskriften "Godkend beregning · måned", PDF-knappen med rapportnummer, "Godkend alle" / "Godkendt" + "Genåbn til rettelser", teksten "Eksport er låst, til alle borgere er godkendt." / eksportknappen, "Tilbage til undtagelser", listen pr. borger og "Tidligere beregninger for måneden" er urørt.
- `koersel/views.py` (visningen `godkend`): fjernet kontekstværdierne `totaler` og `godkendt_antal`. Tjekket med søgning at de ikke bruges i andre skabeloner eller visninger. `data` bruges stadig til `data["linjer"]`.
- `static/css/app.css`: fjernet `.tiles`, `.tile`, `.tile .l` og `.tile .v`. Tjekket at de kun blev brugt af `godkend.html` (også forsiden). `--surface-2` og `.head`/`.sub` bruges andre steder og står.
- `koersel/tests.py`: ny test `test_godkend_skaermen_har_ikke_rapportlinje_forklaring_eller_totaler`. Den kontrollerer før og efter "Godkend alle", at de tre ting ikke står i HTML'en, og at det der skal blive, står der (overskrift, PDF-knap, Godkend alle / Genåbn, eksportlås / eksportknap, Tilbage til undtagelser, begge lister). Ingen eksisterende test pegede på de fjernede dele, så ingen er rettet.
- Ingen nye kommandoer eller indstillinger. Brugersynligt: Godkend-skærmen er enklere (README kan nævne det, hvis den beskriver skærmen med totalerne).

- Rettelse efter test-0003 (F1), commit `5a3e2b2`, kun `koersel/tests.py`: i `test_godkend_skaermen_har_ikke_rapportlinje_forklaring_eller_totaler` er de tre separate påstande om "Løn efter skat", "Træk (lønart 991)" og "Udbetaling (lønart 991)" erstattet af en løkke over alle fem etiketter (Borgere, Løn før skat, Løn efter skat, Træk (lønart 991), Udbetaling (lønart 991)). Den kontrollerer, at ingen står som tile-etiket (`<div class="l">…</div>`), fordi teksterne også står i beregningsgrundlaget pr. borger. Klasse-påstandene (`tiles`, `tile`), "x af y godkendt", "Rapport <id> ·" og forklaringssætningen er uændrede. Kontrollen køres stadig både før og efter "Godkend alle", og kontrollen af det der skal blive er urørt. Skærmen og anden kode er ikke rørt.
- Kørt én gang efter rettelsen: `manage.py test` giver "Ran 73 tests ... OK" (73 af 73 grønne). `manage.py makemigrations --check` giver "No changes detected".

### Hvad er ikke lavet, og hvorfor
- Udseendet er ikke efterprøvet visuelt (ingen browser startet). Kun HTML'ens indhold er kontrolleret via testklienten.
- `docs/BOARD.md`, `docs/decisions/log.md`, opgavefilen og testrapporten er ikke committet, som aftalt. Status er `i-gang`.

### Uklart
- intet. Spærringen i `.venv` (`cache.py.txt`) er løst; `.venv` virkede ved denne kørsel, og jeg har ikke genskabt eller rettet noget i den.
