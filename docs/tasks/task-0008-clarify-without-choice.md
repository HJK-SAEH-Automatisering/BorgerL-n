---
nummer: task-0008
titel: Afklar uden valg giver en besked i stedet for en serverfejl
kilde: interview
status: afsluttet
oprettet: 2026-10-26
---

# task-0008 — Afklar uden valg giver en besked i stedet for en serverfejl

## Hvad og hvorfor
På Gennemse transport kan man afklare en række fra filen ved at vælge en medarbejder i en liste og trykke "Bekræft match". Vælger man ingenting og trykker, går siden i stykker med en serverfejl i stedet for at sige "Vælg en medarbejder i listen." Fejlen fandt udvikleren, da opgaven om at skifte ordet borger til medarbejder blev bygget. Beskeden findes allerede i koden; den bliver aldrig vist.

## Færdig når
- [ ] Trykker man "Bekræft match" uden at have valgt en medarbejder, vises beskeden "Vælg en medarbejder i listen.", og siden bliver stående på Gennemse transport. Der er ingen serverfejl.
- [ ] Vælger man en medarbejder og trykker "Bekræft match", virker det som i dag.
- [ ] Rækken forbliver uafklaret, når intet er valgt, og ingen data ændres.
- [ ] Der er en test for tilfældet uden valg, og testen viser beskeden.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- Visningen for Gennemse transport i `koersel/views.py` slår i dag den valgte medarbejder op, også når feltet er tomt. En tom værdi skal behandles, før der slås op, så den eksisterende besked vises.
- Ingen nye felter, ingen migrering og ingen ændring i skabelonen ud over det der skal til.

## Hvad vi ikke rører
- Matchning på navn og hvilke medarbejdere, der kan vælges.
- "Opret ny medarbejder" og alle andre knapper på skærmen.
- Alle andre skærme.

## Afhænger af
task-0007 — begge ændrer koden og testene på Gennemse transport, og der bygges kun på én opgave ad gangen.

## Beslutninger
- BESLUTTET: Den eksisterende besked "Vælg en medarbejder i listen." bruges — den findes allerede, og teksten følger opgaven om ordet medarbejder. Afvist: en ny tekst.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
Årsagen: i handlingen `afklar` i `gennemse` (`koersel/views.py`) slog koden den valgte medarbejder op med `Borger.objects.filter(pk=request.POST.get("borger"), aktiv=True)`. Den tomme valgmulighed sender `borger=""`, og Django kaster `ValueError: Field 'id' expected a number but got ''`. Det blev en serverfejl, og `messages.error(...)` blev aldrig nået. Et helt manglende felt gav `pk=None`, som returnerer tom, og gik allerede godt.

- `koersel/views.py`: værdien læses først og slås kun op, hvis den består af ASCII-cifre. Ellers er `borger` `None`, og den eksisterende besked "Vælg en medarbejder i listen." vises med `messages.error`. Visningen omdirigerer til `gennemse` som før. Rækken røres ikke, og der skrives ingen auditlog. (Færdig når punkt 1 og 3.) Samme rettelse dækker en ikke-numerisk værdi (fx `abc`), som gav samme `ValueError`.
- `koersel/tests.py`: ny test `test_afklar_uden_valgt_medarbejder_giver_besked_og_aendrer_intet` i `FlowTests`. Den poster `afklar` mod en kørsel med en uafklaret række med tom værdi, helt manglende felt og `abc`. For hver kontrolleres det, at der ikke er serverfejl, at man lander på `gennemse`, at beskeden vises, at rækken stadig er uafklaret (`borger` er `None`, ikke `MATCHET`), og at antallet af auditlog-linjer er uændret. (Punkt 4.) Testen fejlede med 2 fejl (tom værdi og `abc`) uden rettelsen og er grøn med den.
- Valg og "Bekræft match" virker som før (punkt 2). Det er allerede dækket af `test_afklar_raekke_og_gem_rettelser_i_registret`, `test_filens_dage_overlever_gem_uden_individuel_og_manuel_afklaring` og den ukendte-id-test i fladetesten (ca. linje 547-550), så jeg har ikke tilføjet en ny.
- Hele suiten kørt én gang (punkt 5): `Ran 81 tests ... OK`. `makemigrations --check`: `No changes detected`.
- Skabelonen er ikke rørt, ingen migrering, ingen nye felter. Ingen ny kommando eller indstilling til README.
- Udseende er ikke efterprøvet, fordi det kræver en browser. Der er kun testet med HTTP-kald og påstande om HTML.
- Commit: `cbd5be1`.

Fund i de øvrige handlinger i visningen (ikke rørt, som aftalt):
- `linje` i `afklar`: `get_object_or_404(Linje, pk=request.POST.get("linje"), koersel=koersel)` har samme mønster. Tom eller ikke-numerisk `linje` giver `ValueError` og dermed en serverfejl i stedet for 404. Et manglende felt giver 404 som det skal. Skabelonen sender altid et gyldigt `linje`, så det kan kun ske med en forfalsket anmodning. Jeg har ikke kørt det, kun læst koden.
- `gem`: tåler tomme og ugyldige værdier. Afstand læses med `_dec` (ugyldigt eller negativt giver `None`), transport kontrolleres mod listen, og rækkerne med fejl samles i en besked. Ingen fejl fundet.
- `fortsaet` (og alt andet end `afklar` og `gem`): ingen opslag på brugerværdier. Ingen fejl fundet.
- "Opret ny medarbejder" er et link til en anden visning, ikke en handling her. Dér (`borger_ny` i `register/views.py`, linje 36-39) bruges `?linje=` direkte i `get_object_or_404(Linje, pk=...)`. En ikke-numerisk værdi (fx `?linje=abc`) giver samme `ValueError` og en serverfejl. Linket i skabelonen bygger altid værdien af rækkens id, så det rammer kun en håndskrevet adresse. Ikke kørt, kun læst.

### Hvad er ikke lavet, og hvorfor
intet. De to fund med `linje` ovenfor ligger uden for opgaven (den siger "alle andre knapper" og "alle andre skærme" rører vi ikke), så jeg har ikke rettet dem.

### Uklart
intet
