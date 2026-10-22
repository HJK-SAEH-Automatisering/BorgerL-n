---
nummer: mockup-0003
titel: Gennemse transport
status: behandlet
oprettet: 2026-10-22
---

# mockup-0003 — Gennemse transport

## Hvad blev vist
1. Trin 2 for september 2026 med trin-bjælke, filnavn og antal rækker.
2. Gule felter øverst for rækker, der ikke er afklaret: tre rækker fra filen (én matcher flere borgere, to kunne ikke matches). Hver har en rullemenu med mulige borgere, "Bekræft match" og "Opret ny borger".
3. Tabel med borger, afstand og transport. Uafklarede rækker står som "Ikke afklaret". En borger uden transport viser "Ikke angivet". En række viser "navnet forekommer flere gange i filen".
4. Spørgsmålet "Vil du ændre noget?" med valgene "Ja, ret oplysninger" og "Nej, fortsæt". "Ja" åbner afstand og transport som felter. "Gem og fortsæt" gemmer.
5. "Nej, fortsæt" er slået fra, til alle uafklarede rækker er afklaret.

## Hvad slutbrugeren reagerede på
R1. Hele skærmen blev vist for slutbrugeren, som mente, at den ser fint ud indtil videre. Der kommer rettelser løbende. Intet i skitsen er ændret som følge af det.

## Hvad blev valgt fra
intet endnu.

## Hvilke data skærmen forudsætter
Findes i datamodellen i dag (læst fra modelfilerne og skabelonen, ingen værdier):
- Række fra filen: navn i filen, minutter, matchstatus, kandidater, valgt borger, transport, "navnet forekommer flere gange".
- Borger: navn, Tj.nr., afstand i km, transport.
- Transporttyper: kører selv, taxa, ingen udgift.

Findes ikke i dag:
- Intet bekræftet. Skærmen bygger på det samme, som den nuværende skærm viser.

## Gæt
- "Nej, fortsæt" er slået fra, mens der er uafklarede rækker. Valgt fordi usikre match aldrig må gættes. Uklart om den nuværende skærm spærrer.
- En borger uden transport spærrer ikke her; en hjælpetekst siger, at det rettes i næste trin. Valgt frem for at kræve det udfyldt nu.
- Rullemenuen for flertydige rækker viser kun kandidaterne. For rækker uden match viser den et udvalg af borgere fra registret. I skitsen er det to borgere.
- Når en række afklares, tager den afstand og transport fra borgerregisteret, så borgeren straks står i tabellen.
- Skitsen viser 12 af 47 rækker. Ingen filtrering eller søgning i listen.
- Navnene i listen er opdigtede, men de tre uafklarede rækker er de samme som i upload-skitsen (mockup-0002), så flowet hænger sammen.

## Åbent
- Skal tabellen kunne søges eller filtreres, når der er mange borgere?
- Skal en ændring af afstand eller transport kun gælde denne måned, eller altid? I dag gemmes den i registret og gælder derfor altid.
- Skal rækker med flere forekomster af samme navn lægges sammen eller vises hver for sig?

## Afledte numre
intet — alle åbne punkter er afvist eller afgjort uden ændring; se beslutningsloggen.
