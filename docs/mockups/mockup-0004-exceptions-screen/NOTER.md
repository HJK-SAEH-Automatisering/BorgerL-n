---
nummer: mockup-0004
titel: Undtagelser
status: behandlet
oprettet: 2026-10-22
---

# mockup-0004 — Undtagelser

## Hvad blev vist
1. Trin 3 for september 2026 med trin-bjælke, tæller ("x af 11 klar") og forklaring om at rettelser kun gælder denne måned.
2. Tabel pr. borger: navn, timer, afstand, transport, zoner, individuel beregning med antal fremmødedage og en statusmarkering.
3. Zoner og individuel beregning er kun åbne, når transporten er "Kører selv". Fremmødedage er kun åbne, når individuel beregning er sat. Skifter transporten, nulstilles de felter, der ikke længere gælder.
4. Status opdateres, mens der rettes: Klar, Mangler transport, Mangler zone, Mangler dage, Mangler sats. Ved manglende sats er der et link "angiv sats" til borgerens kort.
5. Tre knapper: Tilbage, Gem kladde og Beregn. "Beregn" melder, hvor mange borgere der mangler oplysninger, hvis ikke alle er klar.

## Hvad slutbrugeren reagerede på
R1. Hele skærmen blev vist for slutbrugeren, som mente, at den ser fint ud indtil videre. Der kommer rettelser løbende. Intet i skitsen er ændret som følge af det.

## Hvad blev valgt fra
intet endnu.

## Hvilke data skærmen forudsætter
Findes i datamodellen i dag (læst fra modelfilerne, skabelonen og skærmens script, ingen værdier):
- Række: navn, minutter, transport, zoner, individuel beregning, dage, "navnet forekommer flere gange".
- Borger: navn, afstand i km, om satsen mangler.
- Zoneliste og transporttyper.
- Regler for hvornår en række er klar (som ovenfor).

Findes ikke i dag:
- Intet nyt bekræftet. Skærmen bygger på den nuværende.

## Gæt
- Zonerne er 1-6 i rullemenuen. Valgt ud fra at zonelisten kommer fra stamdata; det rigtige antal er ikke kendt.
- Statusteksterne er taget fra den nuværende skærm; jeg har ikke ændret dem.
- "Angiv sats" sætter i skitsen satsen med det samme, i stedet for at åbne borgerens kort. Valgt for at vise, hvad der sker, når den er rettet.
- Listen viser elleve rækker i én lang tabel. Ingen søgning eller filtrering.
- Navnene er de samme som i de forrige skitser, så flowet hænger sammen.
- Rækker med fejl er ikke løftet til toppen af listen. Valgt for at bevare rækkefølgen fra filen.

## Åbent
- Skal rækker, der mangler noget, kunne vises alene ("vis kun dem, der mangler")?
- Skal "Beregn" føre brugeren til den første række, der mangler noget?
- Skal "Gem kladde" give en synlig bekræftelse eller et tidspunkt for sidste gemning?

## Afledte numre
task-0001 — "Beregn" ruller til første række, der mangler noget. Øvrige punkter er afvist eller afgjort uden ændring; se beslutningsloggen.
