---
nummer: mockup-0002
titel: Upload-skærmen
status: behandlet
oprettet: 2026-10-22
---

# mockup-0002 — Upload-skærmen

## Hvad blev vist
1. Upload for september 2026: trin-bjælke, beskrivelse af filen, et område man kan trække en fil til eller klikke på, og knappen "Læs filen".
2. Meddelelse om at der allerede ligger en fil for måneden, med "Fortsæt med den eksisterende".
3. Hjælpeboks der viser, hvordan filen ser ud (kun navn og timer).
4. Tre fejlvisninger: forkert filtype, kolonner mangler, ugyldige eller tomme timer i bestemte rækker.
5. Efter en vellykket læsning: antal rækker læst, matchet, flere mulige og uden match, og en liste over de rækker der skal afklares, med knap videre til næste trin.

## Hvad slutbrugeren reagerede på
R1. Hele skærmen blev vist for slutbrugeren, som mente, at den ser fint ud indtil videre. Der kommer rettelser løbende. Intet i skitsen er ændret som følge af det.

## Hvad blev valgt fra
intet endnu.

## Hvilke data skærmen forudsætter
Findes i datamodellen i dag (læst fra modelfilerne, ingen værdier):
- Kørsel: måned og filnavn på sidst uploadede fil.
- Række fra filen: rækkenummer, navn i filen, minutter, matchstatus (matchet, ingen match, flere mulige).
- Fejlmeddelelser for filtype, manglende kolonner og filer uden rækker.

Findes ikke i dag:
- Fejlmeddelelse **pr. række** ved ugyldige timer: i dag samles de i én tekst, men skærmen skal kunne pege på bestemte rækker.
- Opsummering af matchresultatet direkte efter upload, med liste over de rækker der skal afklares.
- Hvornår filen blev uploadet, og af hvem (kun filnavn gemmes).

## Gæt
- Efter upload vises en resultatside på samme skærm frem for at gå direkte til næste trin. Valgt for at brugeren kan se, hvor mange der er usikre, før brugeren går videre.
- Filområdet kan både trækkes til og klikkes på. I skitsen vælger en rullemenu, hvilken fil der "vælges", da skitsen ikke læser rigtige filer.
- Trinnet efter upload kaldes "Gennemse transport" og står som trin 2 i bjælken. I kodens trin-bjælke hedder trinnene Upload, Gennemse transport, Undtagelser, Godkend; mine tal følger det.
- Uploades en ny fil, erstattes rækkerne og rettelser fra senere trin. Meddelelsen er tilpasset efter det.
- Fire fiktive eksempler på fejl: de er ikke taget fra rigtige filer.

## Åbent
- Skal brugeren kunne se hvem der sidst uploadede, og hvornår?
- Skal en fil med ugyldige rækker kunne læses alligevel, så de gyldige rækker kommer med?
- Skal måneden kunne vælges her, eller kommer den altid fra dashboardet?

## Afledte numre
task-0001 — "Sidst uploadet" viser navn, dato og klokkeslæt. Øvrige punkter er afvist eller afgjort uden ændring; se beslutningsloggen.
