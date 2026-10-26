---
nummer: task-0012
titel: Rækkerne på Godkend-skærmen skifter ikke plads, når nogle er godkendt
kilde: interview
status: afsluttet
oprettet: 2026-10-26
---

# task-0012 — Rækkerne på Godkend-skærmen skifter ikke plads, når nogle er godkendt

## Hvad og hvorfor
På Godkend-skærmen står tallene ikke på samme sted i alle rækker, når nogle medarbejdere er godkendt og andre ikke. Godkendte rækker mangler knappen "Godkend", så knapkolonnen er smallere dér, og navnekolonnen bliver bredere. Tallene skubbes derfor til højre i de godkendte rækker og til venstre i de andre. Mennesket vil have, at intet skifter plads, når der trykkes "Godkend" på nogle rækker. Mennesket foreslog at fjerne mærket "Afventer"; det er ikke årsagen til forskydningen, men mærket fjernes alligevel, fordi mennesket ønsker det.

## Færdig når
- [ ] Alle kolonner står på præcis samme sted i alle rækker, uanset om medarbejderen er godkendt eller ej. Trykkes "Godkend" på en række, flytter ingen af tallene, mærkerne eller knapperne sig, hverken i den række eller i de andre.
- [ ] Det samme gælder, når "Godkend alle" er trykket, og alle rækker er godkendt.
- [ ] "Beregningsgrundlag" står på samme sted i alle rækker, yderst til højre. Er medarbejderen ikke godkendt, står "Godkend" lige til venstre for den, som nu.
- [ ] Mærkerne "Afventer" og "Godkendt" er begge væk. Statuskolonnen findes ikke længere.
- [ ] Er en medarbejder godkendt, er knappen "Godkend" grøn, og den kan ikke trykkes. Teksten på knappen er stadig "Godkend", så den fylder det samme som på de rækker, der ikke er godkendt. Er medarbejderen ikke godkendt, ser knappen ud og virker som i dag.
- [ ] Hvem der godkendte, og hvornår, kan stadig ses, når man holder musen over den grønne knap, og læses op af skærmlæsere. Det står som oplysning på knappen, som det stod på mærket "Godkendt" før.
- [ ] Pladsen, som mærkerne og statuskolonnen fyldte, bruges til mere luft mellem kolonnerne, så rækkerne er lettere at overskue. Afstanden mellem kolonnerne er tydeligt større end i dag, cirka dobbelt.
- [ ] Knapperne står stadig ved siden af hinanden og går ikke ud over det hvide område.
- [ ] "Godkend", "Godkend alle", "Beregningsgrundlag", advarslerne og resten af skærmen virker som før.
- [ ] Der er en test, der viser, at hverken "Afventer" eller "Godkendt" står som mærke på skærmen, at knappen "Godkend" i en godkendt række er markeret som godkendt og ikke kan trykkes, at den bærer oplysningen om, hvem der godkendte og hvornår, og at rækkerne har samme opbygning, uanset om medarbejderen er godkendt.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- Hver række er sit eget gitter, og knapkolonnen får den bredde, dens indhold fylder. På godkendte rækker er indholdet kun "Beregningsgrundlag", så kolonnen er smallere, og navnekolonnen bliver bredere. Rettelsen er, at alle rækker får samme bredde til knapkolonnen.
- Alle rækker har nu den samme opbygning: knappen "Godkend" og knappen "Beregningsgrundlag". Er medarbejderen godkendt, er "Godkend" en deaktiveret knap med en grøn farve, og teksten er stadig "Godkend". Det giver lige bred knapkolonne i alle rækker uden en pladsholder. Pladsholderen fra det første forsøg fjernes, fordi den ikke længere behøves.
- Mærkerne "Afventer" og "Godkendt" fjernes fra `templates/koersel/godkend.html`, og statuskolonnen fjernes fra rækkens kolonner (`.g4` i `static/css/app.css`). Oplysningen om, hvem der godkendte, og hvornår, flyttes til den grønne knap (titel og læsbar tekst).
- Afstanden mellem kolonnerne øges (`column-gap`) med den plads, statuskolonnen og dens mellemrum frigør. Navnekolonnen bevarer en mindstebredde, og knapkolonnen bevarer sin fulde bredde.
- Den grønne farve findes i forvejen som en farve til det godkendte; brug den, og ret også for mørk tilstand, hvis farverne er defineret dér.
- Ingen ændring af hvad knapperne gør.

## Hvad vi ikke rører
- Beregningsgrundlagets side, godkendelseslogikken og advarslerne.
- Teksten på knapperne.
- Alle andre skærme.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Forskydningen løses ved at alle rækker får samme bredde til knapkolonnen — årsagen er knapkolonnen, ikke mærket "Afventer". Afvist: kun at fjerne mærket, som ikke ville have rettet forskydningen.
- BESLUTTET: Mærket "Afventer" fjernes — mennesket bad om det for at simplificere. Afvist: at beholde det.
- BESLUTTET: Mærket "Godkendt" fjernes også, og i stedet bliver knappen "Godkend" grøn og deaktiveret, når medarbejderen er godkendt — mennesket ændrede ønsket, før opgaven var afsluttet. Det overstyrer det tidligere valg om at beholde "Godkendt". Teksten på knappen er stadig "Godkend", så bredden er den samme i alle rækker. Afvist: at ændre teksten til "Godkendt", som er bredere og ville skubbe kolonnerne igen.
- BESLUTTET: Statuskolonnen fjernes, og pladsen bruges til mere luft mellem kolonnerne — mennesket bad om det. Hvem der godkendte, og hvornår, flyttes til den grønne knap, så oplysningen ikke går tabt.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
Anden runde, efter ændrede krav (commit `dd64e02`; første runde var `5ef6c81`). Første rundes pladsholder og statuskolonne er erstattet.

- `templates/koersel/godkend.html`: mærkerne "Afventer" og "Godkendt" er begge fjernet fra rækkerne, og statuskolonnens `<span>` er fjernet. Knapcellen har i alle rækker de to elementer "Godkend" og "Beregningsgrundlag", i den rækkefølge. Er medarbejderen ikke godkendt (og kørslen ikke godkendt), er "Godkend" formularen med knappen som før. Er medarbejderen godkendt (`r.godkendt`) eller kørslen godkendt, er "Godkend" `<button type="button" disabled class="godkendt" ...>Godkend</button>`. Teksten er stadig "Godkend". `title` og `aria-label` er "Godkendt af <bruger> d.m.Y H:i" (`r.godkendt_af`, `r.godkendt_tidspunkt`); mangler en af dem, står der "Godkendt". Pladsholderen (`<span class="btn plads">`) er fjernet.
- Det samlede mærke `<span class="badge ok">Godkendt</span>` øverst ved "Genåbn til rettelser" er ikke rørt, som aftalt. Advarselsmærkerne (`badge warn`) under rækkerne er heller ikke rørt.
- `static/css/app.css`: `.g4` er nu fem kolonner (`minmax(48px, 1fr) 90px 90px 96px max-content`) med `column-gap: 20px` (før seks kolonner og 10px). Beløbskolonnerne har samme bredder som før, og knapkolonnen er `max-content`. De 80px statuskolonne plus ét mellemrum på 10px er frigjort; luften mellem kolonnerne er fordoblet, og resten går til navnekolonnen. Reglen `.knapper .plads` er fjernet. Ny regel `.knapper button.godkendt, ...:hover, ...:disabled` med `background: var(--ok-bg); color: var(--ok); border-color: var(--ok); cursor: default;`.
- Farverne: `--ok-bg` og `--ok` findes allerede i `:root` og i det mørke tilfælde (`prefers-color-scheme: dark`), og er samme farver som mærket `.ok`, flash-beskeden og `.msg.ok` bruger. Jeg har genbrugt dem, så mørk tilstand følger med uden ekstra regel. Kantfarven er sat til `--ok`; kantbredden (0.5px) og padding er uændrede og arves fra `button, .btn`, så de to knapudgaver har samme padding og kant. Hover-reglen har samme farver, så ingen hover-effekt slår igennem. Regelens `:disabled`-vælger gør, at browserens grå tekst på deaktiverede knapper ikke bruges.
- `koersel/tests.py`: testen er omdøbt til `test_godkendte_og_ikke_godkendte_raekker_har_samme_opbygning_uden_maerker`. Den viser at: ingen række har `badge` eller teksten "Afventer"/"Godkendt" før, midt i og efter godkendelse (selv "Godkendt" i `title` er uden for rækkens tekst); den godkendte rækkes "Godkend" er deaktiveret, har klassen `godkendt`, er ikke en formular eller `submit`, og bærer `title` og `aria-label` med "Godkendt af tester <dato og tid>"; den ikke-godkendte række har den aktive formular og ingen `godkendt`/`disabled`; begge celler har samme to elementer i samme rækkefølge; samme opbygning efter "Godkend alle", hvor det samlede mærke øverst stadig står som det eneste `badge ok`. Ny test `test_den_groenne_godkend_knap_har_egen_farve_uden_hover_og_pladsholderen_er_vaek` (CSS-reglen, hover/disabled, mørk tilstand, ingen `.plads` i CSS eller skabelon, ingen ekstra padding/kantbredde). `test_godkend_og_beregningsgrundlag_staar_i_samme_celle_med_godkend_foerst` er rettet, så godkendte celler har en deaktiveret knap i stedet for en pladsholder. `test_knapkolonnen_har_ingen_fast_bredde_og_knapperne_ombrydes_ikke` kræver nu fem kolonner og `column-gap` på mindst 20px.
- Testresultat, hele suiten én gang: `Ran 93 tests in 27.054s` / `OK`. `makemigrations --check`: `No changes detected`. (Første kørsel i denne runde havde 1 fejl i min egen test af kolonnetællingen, `6 != 5`, fordi `minmax(48px, 1fr)` blev talt som to; rettet.)
- Til README (architect): intet nyt for brugeren ud over at Godkend-skærmen ikke længere har mærkerne "Afventer"/"Godkendt" i rækkerne; en godkendt medarbejder vises i stedet med en grøn, ikke-trykbar "Godkend"-knap, hvor musen over knappen viser hvem og hvornår. Ingen nye kommandoer eller indstillinger.

### Hvad er ikke lavet, og hvorfor
- Udseendet er ikke efterprøvet visuelt (ingen browser startet; kun HTML- og CSS-påstande i testene). Det skal ses af architect eller mennesket: at kolonnerne står præcist ens i alle rækker, at den grønne knap er læsbar (lys og mørk tilstand), at 20px luft ser rigtigt ud, og at knapperne ikke går ud over det hvide område. Ved bredden er jeg gået ud fra, at en deaktiveret `<button>` og den almindelige `<button>` har samme mål (samme padding, kantbredde og skrifttype fra `button, .btn`); det er ikke målt.
- `docs/mockups/mockup-0001-approval-screen/index.html` indeholder stadig "Afventer"; den er en skitse og er ikke rørt.
- Ingen spærring eller karantæne i `.venv` mødt; intet genskabt dér.

### Uklart
intet
