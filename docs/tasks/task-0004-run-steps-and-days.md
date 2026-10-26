---
nummer: task-0004
titel: Trin som knapper i venstre side og antal dage fra Punchly-filen
kilde: interview
status: afsluttet
oprettet: 2026-10-23
---

# task-0004 — Trin som knapper i venstre side og antal dage fra Punchly-filen

## Hvad og hvorfor
Mennesket har gennemgået den kørende webapp og bad om to rettelser.

1. De fire trin i kørslen (Upload, Gennemse transport, Undtagelser, Godkend) står i dag som en række i toppen. De skal stå som knapper i en søjle i venstre side.
2. Vælger man individuel beregning for en borger, skal man i dag skrive antal fremmødedage ind i hånden. Tallet står allerede i Punchly-filen, i kolonnen "Antal arbejdsdage", men importen læser den ikke.

De to er samlet i én opgave, fordi de er små og ligger i de samme skærme. De er uafhængige af hinanden.

## Færdig når
Trinene:

- [ ] På de fire skærme står trinene som knapper i en søjle i venstre side, ved siden af indholdet, og ikke længere som en række i toppen.
- [ ] Hver knap viser nummer og navn som i dag, og alle fire kan trykkes på, som i dag.
- [ ] Det aktuelle trin er tydeligt fremhævet, og de trin der er overstået, er markeret som i dag.
- [ ] På smalle skærme, under cirka 800 pixels bredde, lægger knapperne sig i toppen igen, så indholdet ikke bliver klemt.
- [ ] Forsiden, borgerlisten, borgerformularen og loginsiden ser ud som før.
- [ ] Indholdet på de fire skærme virker som før, og intet er skjult eller klemt ved almindelig bredde.

Antal dage:

- [ ] Importen læser kolonnen "Antal arbejdsdage", hvis filen har den. Hedder kolonnen "Antal dage", læses den også. Der ses bort fra store og små bogstaver og mellemrum omkring navnet. Tallet er den enkelte borgers fremmødedage i måneden.
- [ ] Står der et antal dage for en borger i filen, er feltet for dage i Undtagelser forudfyldt, når individuel beregning vælges for borgeren. Brugeren kan stadig rette tallet, før der trykkes "Beregn".
- [ ] Er cellen tom for en borger, er feltet tomt, som i dag.
- [ ] Mangler kolonnen i filen, virker importen som i dag, uden fejl.
- [ ] Står der noget i cellen, der ikke er et helt tal fra 1 til 31, afvises hele filen med række og værdi i meddelelsen, som for ugyldige timer.
- [ ] En række der afklares manuelt på Gennemse transport, mister ikke dagene fra filen.
- [ ] Vælger man individuel beregning fra, derefter fra igen, står dagene stadig forudfyldt.
- [ ] Beregningen bruger dagene fra feltet, forudfyldt eller rettet. Uden individuel beregning bruges dagene ikke.
- [ ] Hjælpeteksten på Upload-skærmen nævner "Antal arbejdsdage" som en valgfri kolonne.
- [ ] Eksempelfilen, som demodataene laver, har kolonnen med opdigtede dage.

Fælles:

- [ ] Der er tests for de fem første punkter under "Antal dage" og for forudfyldningen.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- **Trinsøjlen.** Den findes i `templates/koersel/_stepper.html`, `templates/base.html` og `static/css/app.css`. Siderne får en to-kolonne-opbygning med søjlen til venstre og indholdet til højre, kun på de fire skærme. Knapperne får udseende som knapper, i samme stil som de øvrige knapper og med de samme farver for aktuelt og overstået trin. Under cirka 800 pixels falder den tilbage til en række i toppen. Skærmenes egne bredder, fx den smalle Upload-skærm, justeres kun hvis det er nødvendigt.
- **Importen.** `koersel/importer.py` finder kolonnen "Antal arbejdsdage" (eller "Antal dage") ved siden af "Navn" og "Total timer" og returnerer dagene for hver række. Kolonnen er valgfri. Ugyldige værdier samles i samme fejlmeddelelse som ugyldige timer.
- **Lagring.** Rækken i kørslen har allerede et felt til dage. Udvikleren vælger, om fildagene gemmes der, eller i et nyt felt ved siden af, så forudfyldningen kan komme igen, når individuel beregning slås til og fra. Hvad der end vælges, må beregningen kun bruge dage, når individuel beregning er valgt. Migreringen laves med `makemigrations`.
- **Forudfyldning.** Skærmkoden i `static/js/undtagelser.js` fylder feltet fra filens tal, når individuel beregning vælges, og feltet er tomt. Reglerne for hvornår en række er klar, er uændrede.
- **Match på Gennemse.** Når en række afklares manuelt, må filens dage ikke nulstilles.
- **Hjælpetekst og eksempelfil.** Teksten på Upload-skærmen og eksempelfilen i `register/management/commands/seed_demo.py` opdateres. Dagene i eksempelfilen er opdigtede.

## Hvad vi ikke rører
- Beregningsmotoren, snapshot, PDF-rapport og eksport.
- Godkendelse og de øvrige trin ud over de to nævnte ændringer.
- Matchning på navn og afklaring af uafklarede rækker, ud over at dagene bevares.
- Forsiden, borgerlisten, borgerformularen, login og administrationssiden.
- Stamdata, zonepriser og parametre.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Én opgave for de to rettelser — de er små, ligger i de samme skærme, og mennesket bad om at få dem samlet. Afvist: to opgaver.
- BESLUTTET: Trinene er stadig alle trykbare, med samme tekst og samme markeringer — mennesket bad kun om ændret placering og udseende. Afvist: at låse senere trin.
- BESLUTTET: Under cirka 800 pixels lægges trinene i toppen — så indholdet ikke bliver klemt på en lille skærm.
- BESLUTTET: Dagene fra filen er et forslag, ikke et facit — de står forudfyldt og kan rettes før Beregn.
- BESLUTTET: Tom celle betyder ikke angivet; ugyldigt tal afviser hele filen — samme regel som for timer, og ingen gætning.
- BESLUTTET: Kolonnen hedder "Antal arbejdsdage" i menneskets fil, og tallet er den enkelte borgers fremmødedage. "Antal dage" læses også — det var det første navn, mennesket nævnte, og det koster intet at acceptere begge. Rettet efter at den første bygning ikke genkendte kolonnen i menneskets testfil.
- BESLUTTET: Kolonnen er valgfri — ældre filer og filer uden kolonnen skal stadig kunne uploades.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
Trinene:
- `templates/base.html`: indholdet ligger nu i en `div.side` med en blok `sideclass`. De fire skærme (`upload.html`, `gennemse.html`, `undtagelser.html`, `godkend.html`) sætter blokken til `med-trin`; de øvrige skærme sætter den ikke og er uændrede.
- `static/css/app.css`: `.side.med-trin` er to kolonner (søjle på 210 px til venstre, indhold til højre, samlet højst 1440 px, indholdet stadig højst 1200 px). `.stp` er nu knapper i samme stil som `button`/`.btn` (kant, afrunding, overflade). Aktuelt trin har samme farver som `.primary`; overståede trin har fuld tekstfarve, kommende trin dæmpet. Under 800 px falder det tilbage til en række i toppen (`@media (max-width: 800px)`).
- `templates/koersel/_stepper.html` er uændret: samme tekster, samme links, alle fire kan trykkes, samme `on`/`done`-klasser.

Antal dage:
- `koersel/importer.py`: finder kolonnen "Antal arbejdsdage" eller "Antal dage" (uden hensyn til store/små bogstaver og mellemrum, også flere mellemrum inde i navnet) i samme overskriftsrække som "Navn" og "Total timer". Rettet efter at menneskets testfil har "Antal arbejdsdage"; første bygning kendte kun "Antal dage". Står begge kolonner i rækken, bruges den første fra venstre. `Raekke` har nyt felt `dage`. Tom celle giver `None`; mangler kolonnen, er alle `None` uden fejl. Heltal 1-31 (også som tekst eller helt flydende tal fra Excel) accepteres; alt andet (0, 32, negative, kommatal, tekst, sand/falsk) giver en fejl i samme samlede meddelelse som ugyldige timer: "Række N (navn): 'værdi' i kolonnen '<overskriften som i filen>' er ikke et gyldigt antal dage (helt tal fra 1 til 31)."
- Lagring: nyt felt `Linje.fil_dage` (`koersel/models.py`, migrering `koersel/migrations/0003_linje_fil_dage.py`). Filens dage gemmes dér og røres aldrig af `saet_borger` eller af skiftet af transport. `Linje.dage` er uændret brugerens værdi, som beregningen bruger, og som som hidtil kun gemmes ved individuel beregning. Derfor bruges filens dage aldrig af beregningen direkte; kun hvad der står i feltet ved Gem/Beregn. `koersel/services.py` (`opret_linjer`) sætter `fil_dage`.
- Forudfyldning: `templates/koersel/undtagelser.html` giver dagsfeltet `data-fil-dage` og viser filens tal serverside, når individuel beregning er valgt og `dage` er tom. `static/js/undtagelser.js` fylder feltet fra `data-fil-dage`, når individuel beregning slås til og feltet er tomt (også efter fra og til igen, da feltet ryddes ved fraslag). Brugeren kan rette tallet. Reglerne for "klar" er uændrede.
- `templates/koersel/upload.html`: hjælpeteksten nævner "Antal arbejdsdage" som valgfri kolonne.
- `register/management/commands/seed_demo.py`: eksempelfilen har kolonnen "Antal arbejdsdage" med opdigtede dage (to tomme celler, Person 5 og 8). Filen `eksempel/punchly-eksempel.xlsx` er genskabt og kan læses (kontrolleret). Mappen er i `.gitignore`.
- Tests i `koersel/tests.py`: importen (kolonne læst under begge navne, store/små bogstaver og mellemrum i overskrift for begge navne, dagskolonne før Navn, tom celle, kolonne mangler, ugyldige værdier for begge navne med kolonnenavnet i meddelelsen), upload gemmer `fil_dage` uden at sætte `dage`, forudfyldning kun ved individuel beregning (tom når filen ingen dage har), rettede dage vinder, filens dage overlever manuel afklaring og Gem uden individuel, hjælpetekst, og beregningen bruger dage kun ved individuel beregning (snapshottet).
- Ingen nye kommandoer eller indstillinger. Brugerens mulige README-punkt: Punchly-filen kan have en valgfri kolonne "Antal arbejdsdage" (eller "Antal dage"), der forudfylder fremmødedage ved individuel beregning.

Kørt efter rettelsen: `manage.py test` (hele suiten, én gang): 72 tests, grøn. `manage.py makemigrations --check`: ingen ændringer. Linter findes ikke i projektet. Rettelsen er committet som `task-0004: læs kolonnen Antal arbejdsdage (og Antal dage) i importen`. `eksempel/punchly-eksempel.xlsx` er genskabt med `seed_demo` og kontrolleret: 13 rækker, dage læst (to tomme).

### Hvad er ikke lavet, og hvorfor
- Udseende og rulning af trinsøjlen og dagsfeltet er ikke efterprøvet visuelt: det kræver en browser, som agenter ikke må starte. Efterprøvet er kun HTML (klasser, blokke, `data-fil-dage`, værdier) og testsuiten. Javascript-forudfyldningen (til/fra/til) er ikke kørt; den serverside forudfyldning er testet. Det bør `architect` eller mennesket se på: søjlens bredde mod Undtagelser-skærmens rækker (`.g3` har faste kolonner på 90 og 150 px) ved 1024-1280 px bredde, Upload-skærmens 720 px smalle indhold midtstillet i højre kolonne, og at knapperne ligger i en række i toppen under 800 px.
- Ellers intet.

### Uklart
- Menneskets rigtige fil er uset af mig, og den er ikke afprøvet; kun opdigtede data i tests. Importen leder efter dagskolonnen i samme række som "Navn" og "Total timer" (inden for de første 50 rækker). Står "Antal arbejdsdage" i en anden række (fx en separat overskriftsrække, eller overskriften står i en sammenflettet celle), findes den ikke, og dagene bliver tavst tomme uden fejl. Overskrifter med andre stavemåder (fx "Arbejdsdage", "Antal arbejdsdage (dage)") genkendes heller ikke. Er det tilfældet i den rigtige fil, så skriv den præcise overskrift og placering til mig.
- Intet blokerende ud over det. To valg, jeg traf inden for opgaven: filens dage ligger i et nyt felt `fil_dage` (opgaven lod mig vælge), og en ny upload erstatter alle rækker og dermed også `fil_dage`, som før. Efter en genåbnet kørsel hvor man ikke uploader igen, findes `fil_dage` stadig.
