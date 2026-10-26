---
nummer: task-0011
titel: Få browseren til at hente nyt stylesheet og ny skærmkode, når de ændres
kilde: interview
status: afsluttet
oprettet: 2026-10-26
---

# task-0011 — Få browseren til at hente nyt stylesheet og ny skærmkode, når de ændres

## Hvad og hvorfor
Siderne henter deres stilark og skærmkode (CSS og JavaScript) fra faste adresser. Browseren kan gemme en gammel udgave og blive ved med at bruge den, også efter at appen er rettet. Det er sket mindst to gange under rettelsen af knapperne på Godkend-skærmen: serveren leverede den nye CSS, men skærmbilledet viste stadig knapperne stablet, som med den gamle. Brugeren skal ikke skulle trykke Ctrl+F5 for at se en rettelse.

## Færdig når
- [ ] Når en CSS- eller JavaScript-fil i appen ændres, får siden en ny adresse til filen, så browseren henter den nye udgave af sig selv.
- [ ] Er filen uændret, er adressen den samme, så browseren stadig kan genbruge den.
- [ ] Det gælder alle sider i appen og både stilarket og skærmkoden på Undtagelser.
- [ ] Der er ingen ny afhængighed, og appen starter som før uden ekstra indstillinger.
- [ ] Siderne ser ud og virker som før.
- [ ] Der er en test, der viser, at adressen til stilarket indeholder en version, at versionen skifter, når filen ændres, og at den er den samme, når filen er uændret.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- Versionen er filens ændringstidspunkt, læst fra filen. Den lægges på adressen som en forespørgselsværdi, fx `?v=...`, i `templates/base.html` og i skabelonen, der henter skærmkoden til Undtagelser. Det kan gøres med en lille skabelonfunktion eller en værdi, der sendes med til alle skabeloner. Metoden vælger udvikleren, så længe den ikke kræver nye pakker.
- Versionen kan læses, hver gang siden vises, eller ved opstart. Læses den ved opstart, følger den kodens opstart. Udvikleren vælger og skriver det i noterne.
- Ingen ændring af hvordan filerne leveres, og ingen ændring af selve stilarket eller skærmkoden.

## Hvad vi ikke rører
- Selve CSS- og JavaScript-filerne.
- Hvordan filerne leveres af serveren og andre indstillinger i `config/settings.py`, medmindre det er nødvendigt.
- Alle skærme og deres indhold.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Filens ændringstidspunkt bruges som version — det kræver ingen pakker og skifter præcis, når filen skifter. Afvist: en pakke til at navngive filer ved hjælp af et fingeraftryk, som kræver et ekstra trin ved hver udrulning.
- BESLUTTET: Opgaven bygges nu, fordi fejlen er set to gange i praksis og har fået mennesket til at tro, at en rettelse ikke virkede.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
- `koersel/templatetags/asset_tags.py` (ny, samt tom `__init__.py`): skabelonfunktionen `static_v`. Den kalder Djangos `static()`, finder filen med `staticfiles.finders.find()` og lægger filens ændringstidspunkt på adressen som `?v=<mtime i nanosekunder>`. Er filen ikke fundet eller kan ikke læses, returneres adressen uden version, så siden ikke fejler.
- `templates/base.html`: stilarket hentes med `{% static_v 'css/app.css' %}` (alle sider arver fra base). `{% load static %}` er skiftet til `{% load asset_tags %}`.
- `templates/koersel/undtagelser.html`: skærmkoden hentes med `{% static_v 'js/undtagelser.js' %}`. `{% load static %}` er skiftet til `{% load asset_tags %}`. Der var ingen andre `{% static %}`-kald i skabelonerne.
- `koersel/test_asset_tags.py` (ny, 7 tests): adressen har `?v=`; samme version når filen er uændret; ny version når ændringstidspunktet ændres (midlertidig mappe via `override_settings(STATICFILES_DIRS=...)` og `os.utime`, projektets egne filer er ikke rørt); manglende fil giver adresse uden version; stilarket har version på Kørsler-siden og loginsiden; både stilark og skærmkode har version på Undtagelser.
- Valg: versionen læses ved hver visning (ét `os.stat` pr. fil pr. side), ikke ved opstart. Serveren kører med `--noreload`, så en opstartsversion ville ikke følge en CSS-ændring uden genstart. Prisen er ét filkald pr. fil pr. visning.
- Ingen ny afhængighed, ingen ændring i `config/settings.py`, ingen indstillinger. Intet til README: en bruger ser ingen ny kommando eller indstilling.
- Testresultat, ordret: `manage.py test` kørt én gang for hele suiten: "Ran 91 tests in 25.752s — OK". `manage.py makemigrations --check`: "No changes detected". Systemtjekket: "no issues (0 silenced)".
- Udseendet er ikke efterprøvet visuelt (ingen browser startet); kun HTML'en er kontrolleret med påstande i tests. At en browser faktisk henter ny CSS efter en ændring, er ikke set.

### Hvad er ikke lavet, og hvorfor
- Færdig-når-punktet "Siderne ser ud og virker som før" er kun efterprøvet ved, at hele suiten er grøn og at selve CSS/JS-filerne ikke er rørt; ikke visuelt, se ovenfor.
- Ingen linter er sat op i projektet, så ingen er kørt.

### Uklart
- Skabelonfunktionen ligger i appen `koersel`, fordi den er den eneste app med skabeloner af den slags, og fordi `base.html` ikke hører til nogen app. Skal den i stedet ligge i `register` eller en egen app, er det en flytning af én fil. Jeg valgte det mindste.
- Under arbejdet blev en baggrundskommando (en tom `python`-heredoc, min egen fejl) hængende i skallen. Den rører ikke projektet. Den ligger som en `python.exe -` (PID 29228 på det tidspunkt) og venter på input; jeg fik afslag på at stoppe den, så den står tilbage og kan stoppes af mennesket. Den lokale server, der kørte i forvejen, er ikke rørt.
