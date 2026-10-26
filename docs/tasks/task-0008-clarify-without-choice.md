---
nummer: task-0008
titel: Afklar uden valg giver en besked i stedet for en serverfejl
kilde: interview
status: planlagt
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
### Hvad er ikke lavet, og hvorfor
### Uklart
