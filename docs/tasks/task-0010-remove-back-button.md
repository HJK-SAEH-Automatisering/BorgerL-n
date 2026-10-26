---
nummer: task-0010
titel: Fjern knappen Tilbage til undtagelser på Godkend-skærmen
kilde: interview
status: afsluttet
oprettet: 2026-10-26
---

# task-0010 — Fjern knappen Tilbage til undtagelser på Godkend-skærmen

## Hvad og hvorfor
Mennesket vil simplificere Godkend-skærmen og har bedt om, at knappen "Tilbage til undtagelser" fjernes. Trinsøjlen i venstre side har allerede en knap til Undtagelser, så vejen tilbage findes stadig.

## Færdig når
- [ ] Knappen "Tilbage til undtagelser" er væk fra Godkend-skærmen, både før og efter at alt er godkendt.
- [ ] Trinsøjlens knap til Undtagelser virker stadig.
- [ ] "Åbn PDF-rapport", "Godkend alle" (eller "Godkendt" og "Genåbn til rettelser"), eksportknappen eller teksten om at eksport er låst, og resten af skærmen er uændret.
- [ ] Der er en test, der viser, at knappen ikke står på skærmen, og at adressen til Undtagelser stadig er med i trinsøjlen.
- [ ] Testsuiten er grøn.

## Sådan bygger vi det
- Knappen står i rækken med knapper øverst i `templates/koersel/godkend.html`. Linjen fjernes. Ingen andre filer skal ændres, medmindre en eksisterende test kontrollerer teksten.

## Hvad vi ikke rører
- Trinsøjlen, Undtagelser-skærmen og alle andre knapper på Godkend-skærmen.
- Godkendelseslogikken og alle andre skærme.

## Afhænger af
intet

## Beslutninger
- BESLUTTET: Kun den ene knap fjernes — mennesket bad kun om den. Vejen tilbage findes i trinsøjlen. Afvist: at fjerne flere knapper uden at spørge.

## Åbne punkter
intet

## Indvendinger
<Udfyldes af andre roller.>

---

## Developers noter

<Alt over denne overskrift ejes af architect. Alt herunder skrives kun af developer, som aldrig retter i definitionen ovenfor.>

### Hvad er lavet
- `templates/koersel/godkend.html`: linjen med knappen "Tilbage til undtagelser" er fjernet fra rækken med knapper. Intet andet i skabelonen er ændret. Det dækker første punkt i Færdig når (både før og efter godkendelse, da knappen stod uden betingelse) og tredje punkt (de øvrige knapper og teksten om eksportlås er urørt).
- `templates/koersel/_stepper.html`: urørt. Trinsøjlens link til Undtagelser er der stadig (andet punkt).
- `koersel/tests.py`: ny test `test_godkend_skaermen_har_ikke_knappen_tilbage_til_undtagelser_men_trinsoejlen_linker_dertil`. Før og efter "Godkend alle" kontrollerer den, at teksten "Tilbage til undtagelser" ikke står, at trinsøjlen har sit link til Undtagelser-adressen, og at adressen kun står én gang på siden. Opdigtede data ("Person 1", "Person 2").
- `koersel/tests.py`: i den eksisterende test `test_godkend_skaermen_har_ikke_rapportlinje_forklaring_eller_totaler` er påstanden `assertContains(svar, "Tilbage til undtagelser")` fjernet, da den ellers ville fejle.
- Testsuiten er kørt én gang (`.venv\Scripts\python.exe manage.py test`): "Ran 84 tests in 14.878s", "OK". `makemigrations --check`: "No changes detected".
- Ingen nye kommandoer eller indstillinger. Brugeren ser, at knappen "Tilbage til undtagelser" ikke længere står på Godkend-skærmen.

### Hvad er ikke lavet, og hvorfor
- Udseendet er ikke efterprøvet visuelt; der er ikke startet nogen browser. Kun HTML'en er kontrolleret gennem testklienten. Om rækken med knapper ser rigtig ud uden den sidste knap, skal øjnene afgøre.

### Uklart
intet
