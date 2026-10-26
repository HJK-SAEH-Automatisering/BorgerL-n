---
nummer: task-0009
titel: Placér knappen Beregningsgrundlag ved siden af Godkend
kilde: interview
status: afsluttet
oprettet: 2026-10-26
---

# task-0009 — Placér knappen Beregningsgrundlag ved siden af Godkend

## Hvad og hvorfor
Mennesket har set knappen "Beregningsgrundlag" på Godkend-skærmen og siger, at den står det forkerte sted. Den skal stå lige ved siden af "Godkend"-knappen, på højre side af rækken. Opgaven om knappen (task-0006) satte den i en kolonne for sig, efter en kolonne til "Godkend", så den kan stå i en afstand fra knappen, og den er bredere end sin kolonne.

## Færdig når
- [ ] På hver række på Godkend-skærmen står "Beregningsgrundlag" lige til højre for "Godkend", på samme linje og med en lille afstand imellem.
- [ ] Er medarbejderen allerede godkendt, så "Godkend" ikke vises, står "Beregningsgrundlag" yderst til højre på rækken, på samme sted som på de rækker, hvor begge knapper står.
- [ ] Knapperne står aldrig over hinanden og går aldrig ud over det hvide område, hverken ved en stor skærm eller et vindue på cirka 1000 pixels. Er der ikke plads, bliver kolonnen med navnet smallere, og knapkolonnen bevarer sin fulde bredde. Det hvide område udvides ikke ud over skærmen; det er navnet, der viger.
- [ ] Knapperne har samme højde og samme udseende som i dag. Teksten på dem er uændret.
- [ ] "Godkend", "Godkend alle", "Beregningsgrundlag", advarslerne og resten af rækken virker som i dag.
- [ ] Der er en test, der viser, at begge knapper står i samme celle på en række, og at "Beregningsgrundlag" står efter "Godkend" i teksten.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- I `templates/koersel/godkend.html` står de to knapper i hver sin celle i rækken. De samles i én celle yderst til højre, med knapperne ved siden af hinanden og med "Godkend" først. Er medarbejderen godkendt, er cellen kun "Beregningsgrundlag".
- Rækkens kolonner i `static/css/app.css` (klassen `.g4`) justeres, så der er én kolonne til de to knapper i stedet for to. Kolonnen får den bredde, knapperne selv fylder (fx `max-content`), så den aldrig er for smal, og navnekolonnen er den, der viger (`minmax(0, 1fr)` med en lille mindstebredde). Cellen retter knapperne til højre. Knapperne står i en række uden ombrydning (`flex-wrap: nowrap`, `white-space: nowrap`). Tjek at ingen anden regel i `app.css` gør cellen smallere, og at `.row` ikke klipper cellen.
- Ingen ændring af hvad knapperne gør, og ingen ændring af den nye side.

## Hvad vi ikke rører
- Beregningsgrundlagets side, godkendelseslogikken og advarslerne.
- Andre skærme.
- Teksten på knapperne.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Knapkolonnen får den bredde, knapperne selv fylder, så den aldrig er for smal — udvikleren målte i første forsøg ikke bredden, og knapperne endte over hinanden. Mennesket sendte et skærmbillede, der viste det. Afvist: en fast bredde i pixels, regnet ud fra skriften.
- BESLUTTET: Er der ikke plads, flyttes "Godkend" til venstre sammen med "Beregningsgrundlag", og navnekolonnen får mindre plads — som mennesket bad om. Afvist: at stable knapperne.
- BESLUTTET: De to knapper samles i én celle — så de altid står ved siden af hinanden, også når "Godkend" ikke vises. Afvist: at flytte kolonnerne rundt uden at samle dem.
- BESLUTTET: Udvikleren kan ikke se skærmen; HTML'ens opbygning og en test kan kontrolleres, men mennesket ser udseendet. Passer det ikke, bliver det en ny opgave.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
- `templates/koersel/godkend.html`: "Godkend"-formularen (kun hvis ikke godkendt) og linket "Beregningsgrundlag" står nu i én celle, `<div class="knapper">`, med "Godkend" først. Er medarbejderen godkendt, indeholder cellen kun "Beregningsgrundlag". Knappernes tekst, formular og link er uændrede. (Færdig når 1, 2, 4, 5)
- `static/css/app.css`: ny regel `.knapper` (flex, `justify-content: flex-end`, `gap: 8px`, `white-space: nowrap`) og `.knapper form { display: inline; margin: 0 }`. `.g4` er ændret fra syv til seks kolonner: `minmax(0, 1.4fr) 100px 100px 110px 90px 250px`. Sidste kolonne rummer begge knapper. (Færdig når 1-3)
- `koersel/tests.py`: ny test `test_godkend_og_beregningsgrundlag_staar_i_samme_celle_med_godkend_foerst`. Den viser for en ikke-godkendt medarbejder, at begge knapper står i samme celle og at "Beregningsgrundlag" står efter "Godkend" i HTML'en, og for en godkendt, at cellen kun har "Beregningsgrundlag" (ingen formular). Opdigtede data (Person 1, Person 2). Den eksisterende test af knappen (`test_godkend_skaermen_har_knap_til_beregningsgrundlag_...`) pegede ikke på cellerne og er uændret og grøn. (Færdig når 6)
- Hele suiten kørt én gang: `Ran 82 tests ... OK`. `makemigrations --check`: `No changes detected`. (Færdig når 7)
- Ingen nye kommandoer eller indstillinger til README.

**Rettelse efter skærmbilledet (anden runde):**
- `static/css/app.css`: `.g4` er nu `minmax(48px, 1fr) 90px 90px 96px 80px max-content` med `column-gap: 10px`. Knapkolonnen er `max-content`, altså den bredde knapperne selv fylder, ikke en fast pixelbredde. Navnekolonnen er den eneste der viger (mindstebredde 48 px). `.knapper` har fået `flex-wrap: nowrap` (ud over de eksisterende `white-space: nowrap`, `justify-content: flex-end`, `gap: 8px`). (Færdig når 1-3)
- Tjekket for andre regler der kunne gøre cellen smallere: `button, .btn` er `display: inline-block` uden bredde, `.row`/`.rows` har ingen `overflow` (intet klippes), `.g4` bruges kun på Godkend-skærmen. Ingen af dem er rørt.
- `koersel/tests.py`: ny test `test_knapkolonnen_har_ingen_fast_bredde_og_knapperne_ombrydes_ikke`. Den læser `app.css` og tjekker at `.g4`s sidste kolonne er `max-content`, at `.knapper` har `flex-wrap: nowrap` og `white-space: nowrap`, og at `godkend.html` ikke sætter en `style` på `.knapper`-cellen. Testen af at begge knapper står i samme celle med Godkend først (fra første bygning) er uændret og grøn.
- Hele suiten kørt én gang efter rettelsen: `Ran 83 tests in 13.937s ... OK`. `makemigrations --check`: `No changes detected`.

**Hvad jeg fandt om årsagen til stablingen:**
- Den fulde regel der gav problemet er `.g4`s sidste kolonne på fast `250px`. Knapperne fylder cirka 81 px ("Godkend") + 8 px mellemrum + 160 px ("Beregningsgrundlag") = cirka 249 px, så 250 px har næsten ingen luft, og rækken var dertil for bred ved et smalt vindue (de øvrige kolonner + mellemrum + rækkens indre margen på 2 x 14 px, som første bygning ikke regnede med). Tallene er skønnede fra skriftstørrelsen, ikke målt.
- Med den nuværende CSS kan `.knapper` (flex, `nowrap`) ikke selv lægge knapperne over hinanden. Det ses derfor kun, hvis browseren stadig bruger en gemt udgave af den gamle `app.css` (den havde syv kolonner og ingen `.knapper`-regel, så cellen endte i en smal kolonne, hvor inline-knapperne ombrydes og stikker ud). Jeg har tjekket med et HTTP-kald at den kørende server leverer den nye CSS, men kan ikke se, hvad menneskets browser har gemt. Prøv først en hård opdatering (Ctrl+F5). Det er en hypotese, ikke bekræftet.

### Hvad er ikke lavet, og hvorfor
- Udseendet er ikke efterprøvet visuelt: jeg må ikke starte en browser. Kolonnebredderne er regnet ud fra skriftstørrelserne (system-ui/Segoe UI, 14 px), ikke målt. Mennesket skal se på skærmen, især at knapperne ikke brydes eller skærer ud ved cirka 1000 px. Testen kontrollerer kun CSS-reglernes opbygning, ikke selve udseendet.
- Cache-busting af `app.css` (fx et versionsnummer på stylesheetet i `templates/base.html`) er ikke lavet, da det ikke står i opgaven. Se hypotesen om gemt CSS nedenfor.
- Media-reglen under 800 px i `app.css` rammer kun trinsøjlen (`.side.med-trin`, `.stepper`), ikke rækkerne, og er ikke rørt. Rækken har ingen særlig tilpasning under 800 px, hverken før eller nu.

### Uklart
- Pladsen ved cirka 1000 px er besvaret af architect: navnekolonnen viger. Jeg har derfor sat tallene til 90/90/96/80 px (var 100/100/110/90), mellemrummet til 10 px, og knapkolonnen til `max-content`. Overslag ved 1000 px: rækkens indre bredde cirka 704 px (efter trinsøjle, sidens margen og rækkens egen margen), faste kolonner cirka 356 px, knapper cirka 250 px, mellemrum 50 px, så navnekolonnen får cirka 48 px, altså kun lige over sin mindstebredde, og lange navne ombrydes i flere linjer. Tallene er skønnede, ikke målt. Er det for trangt i virkeligheden, er det en ny opgave om en anden opbygning (fx to linjer pr. række).
- Skal knapperne ikke stå over hinanden efter min rettelse, og mennesket stadig ser dem stablet, er det sandsynligvis en gemt CSS i browseren (se ovenfor); prøv Ctrl+F5.
